# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from cities_light.models import City
from libros.models import LibrosDisponibles, LibrosPrestados, Libro, LibrosRequest, BibliotecaCompartida, LibrosBibliotecaCompartida, LibrosPrestadosBibliotecaCompartida
from perfiles.models import Perfil
from forms import FormNuevoLibro, FormPedirLibro, NuevaBibliotecaCompartida, EditarBibliotecaCompartida, FormPrestarLibroBCompartida
from redlibros.utils import obtener_perfil, definir_fecha_devolucion


def main(request):
    """
    Muestra un search de libros, las últimas acciones que han tomado los usuarios en la red,
    y algo más
    """
    template = "libros/main.html"
    
    libros = LibrosDisponibles.objects.all()
    context = {'libros': libros}
    return render(request, template, context)


@login_required
def nuevo_libro(request, tipo_dueno, slug):
    template = "libros/nuevo_libro.html"

    if request.method == "POST":
        form = FormNuevoLibro(request.POST)
        
        if form.is_valid():            
            titulo = form.cleaned_data.get("titulo", "")
            autor = form.cleaned_data.get("autor", "")
            imagen = form.cleaned_data.get("imagen", "")
            descripcion = form.cleaned_data.get("descripcion", "")
            disponible = form.cleaned_data.get("disponible", "")

            nuevo_libro = Libro(titulo=titulo, autor=autor, imagen=imagen, descripcion=descripcion)
            nuevo_libro.save()

            if disponible:
                if tipo_dueno == "perfil":
                    # !!! Falta opcionalidad para cambiar ciudad
                    perfil_usuario = obtener_perfil(request.user)
                    libro_disponible_obj = LibrosDisponibles(libro=nuevo_libro, perfil=perfil_usuario, ciudad=perfil_usuario.ciudad)
                    libro_disponible_obj.save()
                    
                    return HttpResponseRedirect(reverse('libros:mi_biblioteca'))
                
                elif tipo_dueno == "biblioteca_compartida":
                    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug)
                    libro_disponible_obj = LibrosBibliotecaCompartida(biblioteca_compartida=biblioteca_compartida, libro=nuevo_libro)
                    libro_disponible_obj.save()

                    return HttpResponseRedirect(reverse('libros:biblioteca_compartida', kwargs={'slug_biblioteca_compartida': slug}))

    else:
        form = FormNuevoLibro()

    context = {'form': form, 'tipo_dueno': tipo_dueno, 'slug': slug}
    return render(request, template, context)


@login_required
def mi_biblioteca(request):
    """
    Muestra los libros que ha subido el usuario, tanto prestados como disponibles
    """
    template = "libros/mi_biblioteca.html"
    perfil_usuario = obtener_perfil(request.user)
    libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=True)
    libros_no_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=False, prestado=False)
    libros_prestados = LibrosPrestados.objects.filter(perfil_dueno=perfil_usuario, devuelto=False)

    context = {
        'libros_disponibles': libros_disponibles,
        'libros_prestados': libros_prestados,
        'libros_no_disponibles': libros_no_disponibles
    }

    return render(request, template, context)


def libros_ciudad(request, slug_ciudad, id_ciudad):
    """
    Recibe como parametro una ciudad y un pais
    """
    template = "libros/libros_ciudad.html"
    ciudad = City.objects.get(pk=id_ciudad)
    libros_disponibles = LibrosDisponibles.objects.filter(ciudad=ciudad, disponible=True)
    bibliotecas_compartidas = BibliotecaCompartida.objects.filter(ciudad=ciudad, eliminada=False)    

    context = {
        'ciudad': ciudad,
        'libros_disponibles': libros_disponibles,
        'bibliotecas_compartidas': bibliotecas_compartidas
        }

    return render(request, template, context)


def libro(request, slug):
    template = "libros/libro.html"
    libro = Libro.objects.get(slug=slug)

    context = {'libro': libro}
    return render(request, template, context)


def libros_usuario(request, username):
    template = "libros/libros_usuario.html"

    libros_disponibles = LibrosDisponibles.objects.filter(username=username)
    libros_prestados = LibrosPrestados.objects.filter(username=username)

    context = {'libros_disponibles': libros_disponibles, 'libros_prestados': libros_prestados}

    return render(request, template, context)


@login_required
def pedir_libro(request, id_libro_disponible):
    template = "libros/pedir_libro.html"
    """
    Recibe un id de un objeto LibrosDisponibles, renderiza un form con un mensaje editable que le va a llegar
    al dueño del libro
    !!! id_libro es un bug pues puede que un libro este disponible en la biblioteca de 2 personas diferentes
    """

    if request.method == "POST":

        form = FormPedirLibro(request.POST)

        if form.is_valid():
            mensaje = form.cleaned_data.get("mensaje", "")
            telefono = form.cleaned_data.get("telefono", "")
            email = form.cleaned_data.get("email", "")
            libro_id = form.cleaned_data.get("libro_id", "")

            libro_request = Libro.objects.get(id=libro_id)
            perfil_envio = obtener_perfil(request.user)
            perfil_recepcion = LibrosDisponibles.objects.get(id=id_libro_disponible).perfil

            request_libro = LibrosRequest(libro=libro_request, perfil_envio=perfil_envio, perfil_recepcion=perfil_recepcion, 
                                          mensaje=mensaje, telefono=telefono, email=email)
            request_libro.save()
            
            return HttpResponseRedirect(reverse('perfiles:perfil_propio'))
    else:

        libro_disponible_obj = LibrosDisponibles.objects.get(id=id_libro_disponible)
    
    form_pedir_libro = FormPedirLibro(initial={'libro_id': libro_disponible_obj.libro.id})

    context = {'libro_disponible': libro_disponible_obj, 'form_pedir_libro': form_pedir_libro}

    return render(request, template, context)


@login_required
def libro_request(request, libro_request_id):
    """
    view en la que el usuario acepta o niega el pedido de préstamo de libro
    """
    template = "libros/libro_request.html"

    libro_request = LibrosRequest.objects.get(id=libro_request_id)

    if request.method == "POST":        
        decision = request.POST.get("prestar", "")
        if decision == "prestado":
            libro_request.aceptado = True
            libro_request.save()

            libro_prestado = LibrosPrestados(libro=libro_request.libro, perfil_receptor=libro_request.perfil_envio,
                                     perfil_dueno=libro_request.perfil_recepcion)
            libro_prestado.save()

            libros_disponibles = LibrosDisponibles.objects.filter(libro=libro_request.libro, perfil=libro_request.perfil_recepcion)

            counter = 0
            for libro in libros_disponibles:
                if counter != 0:
                    break
                else:
                    libro.disponible = False
                    libro.save()
                    counter += 1

            return HttpResponseRedirect(reverse('libros:mi_biblioteca'))

        elif decision == "no_prestar":
            libro_request.aceptado = False
            libro_request.eliminado = True
            libro_request.save()

            return HttpResponseRedirect(reverse('libros:mi_biblioteca'))
    else:
        pass

    libro_request = LibrosRequest.objects.get(id=libro_request_id)

    context = {'libro_request': libro_request}

    return render(request, template, context)


@login_required
def prestar_libro(request, libro_request_id):
    """
    view que muestra un mensaje al usuario que ha aceptado prestar un libro
    """
    template = "libros/prestar_libro.html"

    libro_request = LibrosRequest.objects.get(id=libro_request_id)
    datos_contacto = libro_request.perfil_envio.datos_contacto()

    context = {'libro_request': libro_request, 'datos_contacto': datos_contacto}

    return render(request, template, context)


@login_required
def nueva_biblioteca_compartida(request, slug_ciudad, id_ciudad):

    template = "libros/nueva_biblioteca_compartida.html"

    ciudad = get_object_or_404(City, id=id_ciudad)

    if request.method == "POST":
        form = NuevaBibliotecaCompartida(request.POST)

        if form.is_valid():
            
            biblioteca_compartida = form.save(commit=False)
            biblioteca_compartida.perfil_admin = obtener_perfil(request.user)
            biblioteca_compartida.ciudad = ciudad
            biblioteca_compartida.save()

            return HttpResponseRedirect(reverse('libros:libros_ciudad', kwargs={'slug_ciudad': ciudad.slug, 'id_ciudad': ciudad.id}))

    else:
        form = NuevaBibliotecaCompartida()

    context = {'ciudad': ciudad, 'form': form}

    return render(request, template, context)


def biblioteca_compartida(request, slug_biblioteca_compartida):

    template = "libros/biblioteca_compartida.html"

    perfil_usuario = obtener_perfil(request.user)
    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug_biblioteca_compartida)
    usuario_es_administrador = False
    
    if biblioteca_compartida.perfil_admin == perfil_usuario:
        usuario_es_administrador = True

    context = {'biblioteca_compartida': biblioteca_compartida, 'usuario_es_administrador': usuario_es_administrador}

    return render(request, template, context)


@login_required
def editar_info_bcompartida(request, slug_biblioteca_compartida):

    template = "libros/editar_info_bcompartida.html"

    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug_biblioteca_compartida)

    perfil_usuario = obtener_perfil(request.user)    

    if biblioteca_compartida.perfil_admin != perfil_usuario:
        raise PermissionDenied
    else:
        pass

    if request.method == "POST":
        form = EditarBibliotecaCompartida(request.POST, instance=biblioteca_compartida)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('libros:biblioteca_compartida', 
                kwargs={'slug_biblioteca_compartida': biblioteca_compartida.slug}))
        else:
            print form.errors
    else:
        form = EditarBibliotecaCompartida(initial={
                'nombre': biblioteca_compartida.nombre,
                'direccion': biblioteca_compartida.direccion,
                'imagen': biblioteca_compartida.imagen,
                'hora_apertura': biblioteca_compartida.hora_apertura,
                'hora_cierre': biblioteca_compartida.hora_cierre
            })

    context = {'biblioteca_compartida': biblioteca_compartida, 'form': form}

    return render(request, template, context)


@login_required
def editar_libros_bcompartida(request, slug_biblioteca_compartida):

    template = "libros/editar_libros_bcompartida.html"
    
    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug_biblioteca_compartida)
    libros_disponibles = LibrosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, disponible=True)
    libros_no_disponibles = LibrosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, disponible=False)
    libros_prestados = LibrosPrestadosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida)

    context = {'biblioteca_compartida': biblioteca_compartida, 'libros_prestados': libros_prestados, 'libros_disponibles': libros_disponibles, 
            'libros_no_disponibles': libros_no_disponibles}

    return render(request, template, context)


@login_required
def prestar_libro_bcompartida(request, id_libro_compartido):

    template = "libros/prestar_libro_bcompartida.html"

    libro_disponible_obj = LibrosBibliotecaCompartida.objects.get(id=id_libro_compartido)

    if request.method == "POST":
        form = FormPrestarLibroBCompartida(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('usuario', '')
            tiempo_prestamo = form.cleaned_data.get('tiempo_entrega', '')
            
            # crear LibrosPrestadosBibliotecaCompartida object
            perfil_usuario_prestamo = Perfil.objects.get(usuario__username=username)
            fecha_prestamo = datetime.today()
            fecha_max_devolucion = definir_fecha_devolucion(fecha_prestamo, tiempo_prestamo)
            libro_prestado = LibrosPrestadosBibliotecaCompartida(libro=libro_disponible_obj.libro, perfil_prestamo=perfil_usuario_prestamo, 
                                                                 fecha_max_devolucion=fecha_max_devolucion, biblioteca_compartida=libro_disponible_obj.biblioteca_compartida)
            libro_prestado.save()

            # poner no disponible a LibrosBibliotecaCompartida object
            libro_disponible_obj.disponible = False
            libro_disponible_obj.prestado = True
            libro_disponible_obj.save()

            return HttpResponseRedirect(reverse('libros:editar_libros_bcompartida', kwargs={'slug_biblioteca_compartida': libro_disponible_obj.biblioteca_compartida.slug}))

    else:
        form = FormPrestarLibroBCompartida()

    context = {'form': form, 'libro_compartido': libro_disponible_obj}

    return render(request, template, context)


@login_required
def marcar_no_disponible(request):
    
    if request.is_ajax():
        id_libro_disponible = request.POST.get('id_libro_disp', '')
        tipo = request.POST.get('tipo', '')

        if not id_libro_disponible or not tipo:
            return HttpResponse(status=400)  # Bad Request

        if tipo == "perfil":
            libro_disponible = get_object_or_404(LibrosDisponibles, id=id_libro_disponible)
            libro_disponible.disponible = False
            libro_disponible.save()

        elif tipo == "biblioteca":
            pass

        return HttpResponse("libro marcado como no disponible", status=200)
    else:
        return HttpResponse("No es ajax")


@login_required
def marcar_disponible(request):

    if request.is_ajax():
        id_libro = request.POST.get('id_libro', '')
        tipo = request.POST.get('tipo', '')

        if not id_libro or not tipo:
            return HttpResponse(status=400)  # Bad Request

        if tipo == "perfil":
            libro_no_disponible = get_object_or_404(LibrosDisponibles, id=id_libro)
            libro_no_disponible.disponible = True
            libro_no_disponible.save()

        elif tipo == "biblioteca":
            pass

        return HttpResponse("libro marcado como disponible", status=200)
    else:
        return HttpResponse("No es ajax")


@login_required
def marcar_devuelto(request):

    if request.is_ajax():
        id_libro_prestado = request.POST.get('id_libro', '')
        tipo = request.POST.get('tipo', '')

        if not id_libro_prestado or not tipo:
            return HttpResponse(status=400)  # Bad Request

        if tipo == "perfil":
            libro_prestado = get_object_or_404(LibrosPrestados, id=id_libro_prestado)
            libro_prestado.devuelto = True
            libro_prestado.save()

            libro_no_disponible = LibrosDisponibles.objects.filter(libro=libro_prestado.libro, perfil=libro_prestado.perfil_dueno).first()
            libro_no_disponible.disponible = True
            libro_no_disponible.prestado = False
            libro_no_disponible.save()

        elif tipo == "biblioteca":
            pass

        return HttpResponse("libro marcado como devuelto", status=200)
    else:
        return HttpResponse("No es ajax")
