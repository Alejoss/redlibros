# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from cities_light.models import City
from libros.models import LibrosDisponibles, LibrosPrestados, Libro, LibrosRequest
from forms import FormNuevoLibro, FormPedirLibro
from redlibros.utils import obtener_perfil


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
def nuevo_libro(request):
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
                # !!! Falta opcionalidad para cambiar ciudad
                perfil_usuario = obtener_perfil(request.user)
                libro_disponible_obj = LibrosDisponibles(libro=nuevo_libro, perfil=perfil_usuario, ciudad=perfil_usuario.ciudad)
                libro_disponible_obj.save()
            
            return HttpResponseRedirect(reverse('libros:mi_biblioteca'))
 
    else:
        form = FormNuevoLibro()

    context = {'form': form}
    return render(request, template, context)


@login_required
def mi_biblioteca(request):
    """
    Muestra los libros que ha subido el usuario, tanto prestados como disponibles
    """
    template = "libros/mi_biblioteca.html"
    perfil_usuario = obtener_perfil(request.user)
    libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=True)
    libros_prestados = LibrosPrestados.objects.filter(perfil_dueno=perfil_usuario)

    context = {
        'libros_disponibles': libros_disponibles,
        'libros_prestados': libros_prestados
    }

    return render(request, template, context)


def libros_ciudad(request, slug_ciudad, id_ciudad):
    """
    Recibe como parametro una ciudad y un pais
    """
    template = "libros/libros_ciudad.html"
    ciudad = City.objects.get(pk=id_ciudad)
    libros_disponibles = LibrosDisponibles.objects.filter(ciudad=ciudad, disponible=True)

    context = {
        'ciudad': ciudad,
        'libros_disponibles': libros_disponibles
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
def mensaje_request(request, libro_request_id):
    """
    view en la que el usuario acepta o niega el pedido de préstamo de libro
    """
    template = "libros/libro_request.html"

    libro_request = LibrosRequest.objects.get(id=libro_request_id)

    if request.method == "POST":
        print request.POST.get("prestar", "")
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
