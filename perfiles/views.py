from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from forms import formRegistro, formEditarPerfil
from cities_light.models import City
from libros.models import LibrosRequest, LibrosPrestados, LibrosPrestadosBibliotecaCompartida, LibrosDisponibles
from perfiles.models import Perfil
from redlibros.utils import obtener_perfil, obtener_historial_libros, obtener_avatar_large


def registro(request):
	template = "perfiles/registro.html"

	if request.method == "POST":
		form = formRegistro(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponse("Usuario Guardado", status=201)
	
	else:		
		form = formRegistro()

	context = {
		'form': form
	}
	
	return render(request, template, context)


@login_required
def perfil_propio(request):
	template = "perfiles/perfil_propio.html"
	perfil_usuario = obtener_perfil(request.user)
	libros_perfil = {
		'tiene_requests_pendientes': False,
		'tiene_libros_prestados': False,
		'tiene_libros_pedidos': False
		}

	libros_requests = []
	libros_prestados = []
	libros_prestados_bcompartida = []
	libros_pedidos = []

	if LibrosRequest.objects.filter(perfil_envio=perfil_usuario, aceptado=False, eliminado=False).exists():
		libros_perfil['tiene_libros_pedidos'] = True
		libros_pedidos = LibrosRequest.objects.filter(perfil_envio=perfil_usuario, aceptado=False, eliminado=False)

	if LibrosRequest.objects.filter(perfil_recepcion=perfil_usuario, aceptado=False, eliminado=False).exists():
		libros_perfil['tiene_requests_pendientes'] = True
		libros_requests = LibrosRequest.objects.filter(perfil_recepcion=perfil_usuario, aceptado=False, eliminado=False)

	if LibrosPrestados.objects.filter(perfil_receptor=perfil_usuario, fecha_devolucion=None).exists():
		libros_perfil['tiene_libros_prestados'] = True
		libros_prestados = LibrosPrestados.objects.filter(perfil_receptor=perfil_usuario, fecha_devolucion=None)

	if LibrosPrestadosBibliotecaCompartida.objects.filter(perfil_prestamo=perfil_usuario, fecha_devolucion=None).exists():
		libros_perfil['tiene_libros_prestados'] = True
		libros_prestados_bcompartida = LibrosPrestadosBibliotecaCompartida.objects.filter(perfil_prestamo=perfil_usuario, fecha_devolucion=None)

	libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=True, prestado=False)

	avatar = obtener_avatar_large(perfil_usuario)

	context = {'libros_perfil': libros_perfil, 'libros_requests': libros_requests, 'libros_prestados': libros_prestados,
	           'libros_pedidos': libros_pedidos, 'libros_prestados_bcompartida': libros_prestados_bcompartida, 
	           'libros_disponibles': libros_disponibles, 'avatar': avatar}
	
	return render(request, template, context)


def perfil_usuario(request, username):
	template = "perfiles/perfil_usuario.html"
	libros_perfil = {'tiene_libros_prestados': False, 'tiene_libros_disponibles': False}

	# redirigir a la pagina perfil_propio si es el caso
	user_obj = User.objects.get(username=username)
	if user_obj == request.user:
		return HttpResponseRedirect(reverse('perfiles:perfil_propio'))

	perfil = Perfil.objects.get(usuario__username=username)
	historial_libros = obtener_historial_libros(perfil)
	libros_prestados = libros_prestados_bcompartida = libros_disponibles = []

	if LibrosPrestados.objects.filter(perfil_receptor=perfil, fecha_devolucion=None).exists():
		libros_perfil['tiene_libros_prestados'] = True
		libros_prestados = LibrosPrestados.objects.filter(perfil_receptor=perfil, fecha_devolucion=None)

	if LibrosPrestadosBibliotecaCompartida.objects.filter(perfil_prestamo=perfil, fecha_devolucion=None).exists():
		libros_perfil['tiene_libros_prestados'] = True
		libros_prestados_bcompartida = LibrosPrestadosBibliotecaCompartida.objects.filter(perfil_prestamo=perfil, fecha_devolucion=None)

	if LibrosDisponibles.objects.filter(perfil=perfil, disponible=True, prestado=False).exists():
		libros_perfil['tiene_libros_disponibles'] = True
		libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil, disponible=True, prestado=False)

	avatar = obtener_avatar_large(perfil)

	context = {'libros_prestados': libros_prestados, 'libros_prestados_bcompartida': libros_prestados_bcompartida, 'libros_disponibles': libros_disponibles,
	           'historial_libros': historial_libros, 'libros_perfil': libros_perfil, 'perfil': perfil, 'avatar': avatar}

	return render(request, template, context)


@login_required
def logout_view(request):
	logout(request)

	return HttpResponseRedirect(reverse('libros:main'))


@login_required
def editar_perfil(request):
	template = "perfiles/editar_perfil.html"
	perfil_usuario = obtener_perfil(request.user)

	if request.method == "POST":
		form = formEditarPerfil(request.POST, instance=perfil_usuario)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('perfiles:perfil_propio'))

	else:
		if perfil_usuario.ciudad:
			ciudad_default = perfil_usuario.ciudad
		else:
			ciudad_default = City.objects.get(name="Quito")
		form = formEditarPerfil(
			initial={
				'descripcion': perfil_usuario.descripcion,
				'ciudad': ciudad_default,
				'numero_telefono_contacto': perfil_usuario.numero_telefono_contacto
			})

	context = {'form': form}

	return render(request, template, context)
