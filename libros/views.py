# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from libros.models import LibrosDisponibles, LibrosPrestados, Libro
from forms import FormNuevoLibro
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


def mi_biblioteca(request):
    """
    Muestra los libros que ha subido el usuario, tanto prestados como disponibles
    """
    template = "libros/mi_biblioteca.html"
    perfil_usuario = obtener_perfil(request.user)
    libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario)
    libros_prestados = LibrosPrestados.objects.filter(perfil_dueno=perfil_usuario)

    context = {
        'libros_disponibles': libros_disponibles,
        'libros_prestados': libros_prestados
    }

    return render(request, template, context)


def libros_ciudad(request, slug_ciudad):
    """
    Recibe como parametro una ciudad y un pais
    """
    template = "libros/libros_ciudad.html"
    ciudad = City.objects.get(slug=slug_ciudad)
    libros = LibrosDisponibles.objects.filter(ciudad=ciudad)

    context = {
        'ciudad': ciudad,
        'libros': libros
        }

    return render(request, template, context)


def libro(request, slug):
    template = "libros/libro.html"
    libro = Libro.objects.get(slug=slug)

    context = {'libro': libro}
    return render(request, template, context)


def libros_usuario(request, username):
    template = "libros/libros_usuario.html"

    libros_disponibles = LibrosDisponibles.objects.filter(username= username)
    libros_prestados = LibrosPrestados.objects.filter(username=username)

    context = {'libros_disponibles': libros_disponibles, 'libros_prestados': libros_prestados}

    return render(request, template, context)
