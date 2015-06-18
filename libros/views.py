# -*- coding: utf-8 -*-
import re
from django.db.models import Q

from datetime import datetime

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags

from cities_light.models import City
from libros.models import LibrosDisponibles, LibrosPrestados, Libro, LibrosRequest, BibliotecaCompartida, \
                          LibrosBibliotecaCompartida, LibrosPrestadosBibliotecaCompartida
from perfiles.models import Perfil
from forms import FormNuevoLibro, FormPedirLibro, NuevaBibliotecaCompartida, EditarBibliotecaCompartida, FormPrestarLibroBCompartida
from redlibros.utils import obtener_perfil, definir_fecha_devolucion, obtenerquito, mail_pedir_libro, mail_anunciar_devolucion, \
                            mail_aceptar_prestamo, obtener_avatar_large, obtener_historial_libros


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
def nuevo_libro(request, tipo_dueno, username):
    template = "libros/nuevo_libro.html"

    if request.method == "POST":
        form = FormNuevoLibro(request.POST)
        
        if form.is_valid():            
            titulo = form.cleaned_data.get("titulo", "")
            autor = form.cleaned_data.get("autor", "")            
            descripcion = form.cleaned_data.get("descripcion", "")
            disponible = form.cleaned_data.get("disponible", "")

            nuevo_libro = Libro(titulo=titulo, autor=autor, descripcion=descripcion)
            nuevo_libro.save()

            if disponible:
                if tipo_dueno == "perfil":
                    # !!! Falta opcionalidad para cambiar ciudad
                    perfil_usuario = obtener_perfil(request.user)
                    # !!! Todos los libros son marcados disponibles en Quito !!!
                    quito = obtenerquito()
                    libro_disponible_obj = LibrosDisponibles(libro=nuevo_libro, perfil=perfil_usuario, ciudad=quito)
                    libro_disponible_obj.save()
                    
                    return HttpResponseRedirect(reverse('libros:mi_biblioteca'))
                
                elif tipo_dueno == "biblioteca_compartida":
                    slug = username  # fea manera de tomar el argumento y usarlo para biblioteca_compartida
                    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug)
                    libro_disponible_obj = LibrosBibliotecaCompartida(biblioteca_compartida=biblioteca_compartida, libro=nuevo_libro)
                    libro_disponible_obj.save()

                    return HttpResponseRedirect(reverse('libros:biblioteca_compartida', kwargs={'slug_biblioteca_compartida': slug}))

    else:
        form = FormNuevoLibro()

    context = {'form': form, 'tipo_dueno': tipo_dueno, 'username': username}
    return render(request, template, context)


@login_required
def mi_biblioteca(request):
    """
    Muestra los libros que ha subido el usuario, tanto prestados como disponibles
    """
    template = "libros/mi_biblioteca.html"
    perfil_usuario = obtener_perfil(request.user)
    libros_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=True, prestado=False)
    libros_no_disponibles = LibrosDisponibles.objects.filter(perfil=perfil_usuario, disponible=False, prestado=False)
    libros_prestados = LibrosPrestados.objects.filter(perfil_dueno=perfil_usuario, fecha_devolucion=None)

    context = {
        'libros_disponibles': libros_disponibles,
        'libros_prestados': libros_prestados,
        'libros_no_disponibles': libros_no_disponibles
    }

    return render(request, template, context)


def libros_ciudad(request, slug_ciudad, id_ciudad, filtro):
    """
    Recibe como parametro una ciudad, un id de la ciudad y un filtro. 
    renderea un html con los libros ordenados por el filtro
    """

    template = "libros/libros_ciudad.html"
    ciudad = City.objects.get(pk=id_ciudad)    

    if filtro == "autor":
        lista_libros_disponibles = LibrosDisponibles.objects.filter(ciudad=ciudad, disponible=True, prestado=False).order_by("libro__autor")
    else:
        lista_libros_disponibles = LibrosDisponibles.objects.filter(ciudad=ciudad, disponible=True, prestado=False)

    bibliotecas_compartidas = BibliotecaCompartida.objects.filter(ciudad=ciudad, eliminada=False)

    # paginator
    paginator = Paginator(lista_libros_disponibles, 100)

    page = request.GET.get("page")
    
    try:
        libros_disponibles = paginator.page(page)
    
    except PageNotAnInteger:
        libros_disponibles = paginator.page(1)

    except EmptyPage:
        libros_disponibles = paginator.page(paginator.num_pages)

    context = {
        'filtro': filtro,
        'ciudad': ciudad,
        'libros_disponibles': libros_disponibles,
        'paginator': paginator,
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


def buscar_ciudad(request):
    template = "libros/buscar_ciudad.html"

    if request.method == "POST":
        id_ciudad = request.POST.get("ciudades", "")
        set_city = request.POST.get("set_city", "")

        ciudad = City.objects.get(id=id_ciudad)

        if set_city:
            perfil_usuario = obtener_perfil(request.user)
            perfil_usuario.ciudad = ciudad
            perfil_usuario.save()

        return HttpResponseRedirect(reverse('libros:libros_ciudad', kwargs={'slug_ciudad': ciudad.slug, 'id_ciudad': ciudad.id, 'filtro': 'titulo'}))

    ciudades = City.objects.all()
    nombres_ciudades_importantes = ["Quito", "Guayaquil", "Cuenca"]
    ciudades_importantes = []

    for nombre in nombres_ciudades_importantes:
        ciudad = City.objects.get(name=nombre)
        ciudades_importantes.append(ciudad)

    context = {'ciudades': ciudades, 'ciudades_importantes': ciudades_importantes}

    return render(request, template, context)


@login_required
def pedir_libro(request, id_libro_disponible):
    template = "libros/pedir_libro.html"
    """
    Recibe un id de un objeto LibrosDisponibles, renderiza un form con un mensaje editable que le va a llegar
    al dueño del libro    
    """
    perfil_usuario = obtener_perfil(request.user)

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

            if perfil_recepcion.usuario.email:    
                mail_pedir_libro(request_libro, mensaje)

            return HttpResponseRedirect(reverse('perfiles:perfil_propio'))
        else:
            print "form not valid!"
    
    libro_disponible_obj = LibrosDisponibles.objects.get(id=id_libro_disponible)
    
    form_pedir_libro = FormPedirLibro(initial={
        'libro_id': libro_disponible_obj.libro.id,
        'telefono': perfil_usuario.numero_telefono_contacto,
        'email': request.user.email
        })

    avatar = obtener_avatar_large(libro_disponible_obj.perfil)

    context = {'libro_disponible': libro_disponible_obj, 'form_pedir_libro': form_pedir_libro, 'avatar': avatar}

    return render(request, template, context)


@login_required
def libro_request(request, libro_request_id):
    """
    view en la que el usuario acepta o niega el pedido de préstamo de libro
    """
    template = "libros/libro_request.html"
    libro_request = get_object_or_404(LibrosRequest, id=libro_request_id, eliminado=False)

    if request.user != libro_request.perfil_recepcion.usuario:
        raise PermissionDenied

    if request.method == "POST":        
        decision = request.POST.get("prestar", "")
        if decision == "prestado":
            libro_request.aceptado = True
            libro_request.save()
            mensaje = strip_tags(request.POST.get("mensaje_aceptacion", ""))
            tiempo_prestamo = request.POST.get("tiempo_max_devolucion", "")
            fecha_max_devolucion = definir_fecha_devolucion(datetime.today(), tiempo_prestamo)

            fecha_prestamo = datetime.today()
            libro_prestado = LibrosPrestados(libro=libro_request.libro, perfil_receptor=libro_request.perfil_envio,
                                     perfil_dueno=libro_request.perfil_recepcion, fecha_prestamo=fecha_prestamo, mensaje_aceptacion=mensaje,
                                     fecha_max_devolucion=fecha_max_devolucion)
            libro_prestado.save()

            libro_disponible_obj = LibrosDisponibles.objects.filter(libro=libro_request.libro, perfil=libro_request.perfil_recepcion).first()
            libro_disponible_obj.disponible = False
            libro_disponible_obj.prestado = True

            libro_disponible_obj.save()

            if libro_prestado.perfil_receptor.usuario.email:                
                mail_aceptar_prestamo(libro_prestado)

            return HttpResponseRedirect(reverse('libros:mi_biblioteca'))

        elif decision == "no_prestar":
            libro_request.aceptado = False
            libro_request.eliminado = True
            libro_request.save()

            return HttpResponseRedirect(reverse('libros:mi_biblioteca'))
    else:
        pass

    perfil_request = libro_request.perfil_envio

    historial_libros = obtener_historial_libros(perfil_request)
    avatar = obtener_avatar_large(perfil_request)

    ldisponibles_perfil_request = LibrosDisponibles.objects.filter(perfil=perfil_request, disponible=True, prestado=False).count()

    context = {'libro_request': libro_request, 'avatar': avatar, 'historial_libros': historial_libros, 
               'ldisponibles_perfil_request': ldisponibles_perfil_request}

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

            return HttpResponseRedirect(reverse('libros:libros_ciudad', kwargs={'slug_ciudad': ciudad.slug, 'id_ciudad': ciudad.id, 'filtro': 'titulo'}))

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

    libros_bcompartida = LibrosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, disponible=True, prestado=False)
    num_libros_bcompartida = libros_bcompartida.count()

    context = {'biblioteca_compartida': biblioteca_compartida, 'usuario_es_administrador': usuario_es_administrador,
               'libros_bcompartida': libros_bcompartida, 'num_libros_bcompartida': num_libros_bcompartida}

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
                'imagen': biblioteca_compartida.imagen                
            })

    context = {'biblioteca_compartida': biblioteca_compartida, 'form': form}

    return render(request, template, context)


@login_required
def editar_libros_bcompartida(request, slug_biblioteca_compartida):

    template = "libros/editar_libros_bcompartida.html"
    
    biblioteca_compartida = BibliotecaCompartida.objects.get(slug=slug_biblioteca_compartida)
    libros_disponibles = LibrosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, disponible=True, prestado=False)
    libros_no_disponibles = LibrosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, disponible=False, prestado=False)
    libros_prestados = LibrosPrestadosBibliotecaCompartida.objects.filter(biblioteca_compartida=biblioteca_compartida, fecha_devolucion=None)

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
            libro_disponible_obj = get_object_or_404(LibrosBibliotecaCompartida, id=id_libro_disponible)
            libro_disponible_obj.disponible = False
            libro_disponible_obj.save()

        return HttpResponse("libro marcado como no disponible", status=200)
    else:
        return HttpResponse("No es ajax")


@login_required
def marcar_disponible(request):

    if request.is_ajax():
        print "request ajax a marcar_disponible"

        id_libro = request.POST.get('id_libro', '')
        tipo = request.POST.get('tipo', '')

        if not id_libro or not tipo:
            return HttpResponse(status=400)  # Bad Request

        if tipo == "perfil":
            libro_no_disponible = get_object_or_404(LibrosDisponibles, id=id_libro)
            libro_no_disponible.disponible = True
            libro_no_disponible.save()

            return HttpResponse("libo marcado como disponible", status=200)

        elif tipo == "biblioteca":
            print "marcar_disponible id_libro, tipo: %s, %s" % (id_libro, tipo)
            libro_bcompartida_obj = get_object_or_404(LibrosBibliotecaCompartida, id=id_libro)
            libro_bcompartida_obj.disponible = True
            libro_bcompartida_obj.save()

            return HttpResponse("libro marcado como disponible", status=200)
    else:
        return HttpResponse("No es ajax")


@login_required
def marcar_devuelto(request):

    if request.is_ajax():
        id_libro_prestado = request.POST.get('id_libro', '')
        tipo = request.POST.get('tipo', '')
        fecha_devolucion = datetime.today()

        if not id_libro_prestado or not tipo:
            return HttpResponse(status=400)  # Bad Request

        if tipo == "perfil":
            libro_prestado = get_object_or_404(LibrosPrestados, id=id_libro_prestado)
            libro_prestado.devuelto = True
            libro_prestado.fecha_devolucion = fecha_devolucion
            libro_prestado.save()

            libro_no_disponible = LibrosDisponibles.objects.filter(libro=libro_prestado.libro, perfil=libro_prestado.perfil_dueno).first()
            libro_no_disponible.disponible = True
            libro_no_disponible.prestado = False
            libro_no_disponible.save()

        elif tipo == "biblioteca":            
            libro_prestado = get_object_or_404(LibrosPrestadosBibliotecaCompartida, id=id_libro_prestado)
            libro_prestado.fecha_devolucion = fecha_devolucion
            libro_prestado.save()

            libro_no_disponible = LibrosBibliotecaCompartida.objects.filter(libro=libro_prestado.libro, biblioteca_compartida=libro_prestado.biblioteca_compartida).first()
            libro_no_disponible.disponible = True
            libro_no_disponible.prestado = False
            libro_no_disponible.save()

        return HttpResponse("libro marcado como devuelto", status=200)
    else:
        return HttpResponse("No es ajax")


@login_required
def anunciar_devolucion(request):

    if request.method == "POST":
        id_libro_prestado = request.POST.get("id_libro_prestado")
        perfil_usuario = obtener_perfil(request.user)
        libro_prestado = LibrosPrestados.objects.get(id=id_libro_prestado)

        if libro_prestado.perfil_receptor != perfil_usuario:
            raise PermissionDenied
        else:
            libro_prestado.receptor_anuncio_devolucion = True
            libro_prestado.save()

            print libro_prestado.perfil_dueno.usuario
            print "email usuario: %s" % (libro_prestado.perfil_dueno.usuario.email)
            if libro_prestado.perfil_dueno.usuario.email:
                print "enviar mail devolucion"
                mail_anunciar_devolucion(libro_prestado)

        return HttpResponseRedirect(reverse('perfiles:perfil_propio'))
    else:
        raise PermissionDenied 


@login_required
def cancelar_pedido(request):

    if request.method == "POST":
        request_id = request.POST.get("request_id", "")
        perfil_usuario = obtener_perfil(request.user)
        libro_request = LibrosRequest.objects.get(id=request_id)

        if libro_request.perfil_envio != perfil_usuario:
            raise PermissionDenied
        else:
            libro_request.eliminado = True
            libro_request.save()

            return HttpResponse("request de libro cancelado", status=200)
    else:
        raise PermissionDenied


# Para el search de temas
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


# Para el search de temas
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def buscar(request, slug_ciudad, filtro):
    template = 'libros/busqueda.html'
    
    query_string = ""
    libros_disponibles = None

    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        if query_string:
            if filtro == "autor":
                libros_disponibles = LibrosDisponibles.objects.filter(libro__autor__icontains=query_string)
            else:
                libros_disponibles = LibrosDisponibles.objects.filter(libro__titulo__icontains=query_string)

        context = {'query_string': query_string,
                   'libros_disponibles': libros_disponibles,
                   'filtro': filtro,
                   'ciudad': slug_ciudad.capitalize()}
        return render(request, template, context)
    else:
        return redirect('libros:libros_ciudad', slug_ciudad='quito', id_ciudad=18, filtro='titulo')


@login_required
def cambiar_dueno_libros(request):
    template = 'cambiar_dueno_libro.html'

    if not request.user.is_superuser:
        raise PermissionDenied

    libros_ids = request.session['libros']
    libros = []

    for l_id in libros_ids:
        libro = LibrosDisponibles.objects.get(id=l_id)
        libros.append(libro)

    if request.method == "POST":

        nuevo_usuario = request.POST.get('nuevo_dueno', '')

        if nuevo_usuario:
            perfil_dueno = Perfil.objects.get(usuario__username=nuevo_usuario)

            for libro in libros:
                libro.perfil = perfil_dueno
                libro.save()

            return redirect('admin:index')

        else:
            pass

    perfiles = Perfil.objects.all()

    context = {'libros': libros, 'perfiles': perfiles}

    return render(request, template, context)
