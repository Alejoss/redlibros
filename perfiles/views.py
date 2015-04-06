from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from forms import formRegistro, formEditarPerfil
from libros.models import LibrosRequest, LibrosPrestados
from redlibros.utils import obtener_perfil


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
	tiene_requests_pendientes = False
	tiene_libros_prestados = False
	libros_requests = []
	libros_prestados = []

	if LibrosPrestados.objects.filter(perfil_receptor=perfil_usuario).exists():
		tiene_libros_prestados = True
		libros_prestados = LibrosPrestados.objects.filter(perfil_receptor=perfil_usuario)

	if LibrosRequest.objects.filter(perfil_recepcion=perfil_usuario).exists():
		tiene_requests_pendientes = True
		libros_requests = LibrosRequest.objects.filter(perfil_recepcion=perfil_usuario)

	context = {'tiene_requests_pendientes': tiene_requests_pendientes, 'libros_requests': libros_requests,
	           'tiene_libros_prestados': tiene_libros_prestados, 'libros_prestados': libros_prestados}
	
	return render(request, template, context)


def perfil_usuario(request):
	template = "perfiles/perfil.html"
	datos_perfil = ""

	context = {'datos_perfil': datos_perfil}
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
		form = formEditarPerfil(
			initial={
				'descripcion': perfil_usuario.descripcion,
				'ciudad': perfil_usuario.ciudad,
				'numero_telefono_contacto': perfil_usuario.numero_telefono_contacto
			})

	context = {'form': form}

	return render(request, template, context)













