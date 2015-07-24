# -*- coding: utf-8 -*-
import datetime

from django.core.mail import send_mail
from django.template.loader import render_to_string

from perfiles.models import Perfil
from libros.models import LibrosPrestados, LibrosPrestadosBibliotecaCompartida
from cities_light.models import City


# Devuelve el modelo de Quito
def obtenerquito():
	return City.objects.get(id=18)


# Perfil y Editar Perfil
def obtener_avatar_large(perfil):
    # Obtiene un perfil y devuelve la imagen de perfil grande.
    avatar_large = None
    if perfil.imagen_perfil is not None:
        if "facebook" in perfil.imagen_perfil:
            avatar_large = "%s?type=large" % (perfil.imagen_perfil)        
        elif "google" in perfil.imagen_perfil:
            avatar_large = (perfil.imagen_perfil).replace("sz=50", "sz=400")
        else:
            avatar_large = perfil.imagen_perfil
    else:
        avatar_large = "https://s3.amazonaws.com/epona/assets/images/letrasclub/books_biblioteca.jpg"

    return avatar_large


def obtener_perfil(usuario):
	perfil, created = Perfil.objects.get_or_create(usuario=usuario)

	return perfil


def definir_fecha_devolucion(fecha_prestamo, tiempo_prestamo):
	fecha_devolucion = None
	if tiempo_prestamo == "2_semanas":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=3)
	elif tiempo_prestamo == "1_mes":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=5)
	elif tiempo_prestamo == "2_meses":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=9)
	elif tiempo_prestamo == "3_meses":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=13)
	else:
		pass

	return fecha_devolucion


def obtener_historial_libros(perfil):

	libros_recibidos_usuario = LibrosPrestados.objects.filter(perfil_receptor=perfil)
	libros_recibidos_bcompartida = LibrosPrestadosBibliotecaCompartida.objects.filter(perfil_prestamo=perfil)
	libros_prestados_por_usuario = LibrosPrestados.objects.filter(perfil_dueno=perfil)

	return {'libros_recibidos_usuario': libros_recibidos_usuario, 'libros_recibidos_bcompartida': libros_recibidos_bcompartida, 
	'libros_prestados_por_usuario': libros_prestados_por_usuario}


def crear_perfil(backend, user, response, *args, **kwargs):
	"""
	Pipeline de Python Social Auth, crea el perfil y le asigna un avatar que extrae de la red social
	"""
	perfil, creado = Perfil.objects.get_or_create(usuario=user)

	perfil.ciudad = obtenerquito()
	
	if backend.name == "facebook":
		imagen_url_backend = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
		perfil.imagen_perfil = imagen_url_backend
		perfil.save()

	elif backend.name == "google-oauth2":
		if response['image'].get('url') is not None:
			imagen_url_backend = response['image'].get('url')
			perfil.imagen_perfil = imagen_url_backend
			perfil.save()

	return None


def mail_pedir_libro(request_libro, mensaje):
	"""
	Envía un mail al dueño del libro notificándole del pedido
	"""

	titulo = "%s te ha pedido un libro" % (request_libro.perfil_envio.usuario.username)
	mensaje_texto = ("%s te ha pedido que le prestes el libro %s, por favor visita tu perfil en Letras.Club" 
		% (request_libro.perfil_recepcion.usuario.username, request_libro.libro.titulo))
	html_message = render_to_string("pedir_libro_mail.html", {'usuario_receptor_mail': request_libro.perfil_recepcion.usuario.username, 
				'nombre_usuario_envio': request_libro.perfil_envio.usuario.username, 'mensaje': mensaje,
				'titulo_libro': request_libro.libro.titulo, 'autor_libro': request_libro.libro.autor, 'telefono': request_libro.telefono})

	send_mail(
			subject=titulo,
			message=mensaje_texto,
			from_email="letras.club@no-reply.com",
			recipient_list=[request_libro.perfil_recepcion.usuario.email],
			fail_silently=True,
			html_message=html_message
		)

	return None


def mail_anunciar_devolucion(libro_prestado):
	"""
	Envía un mail al dueño del libro notificándole que el usuario que lo recibió
	ya lo marcó como devuelto
	"""

	titulo = "%s ha marcado un libro tuyo como devuelto" % (libro_prestado.perfil_receptor.usuario.username)
	mensaje_texto = ("%s ha marcado tu libro %s como devuelto, si ya lo tienes,\
	 por favor visita tu biblioteca en Letras.Club") % (libro_prestado.perfil_receptor.usuario.username, libro_prestado.libro.titulo)
	html_message = render_to_string("anunciar_devolucion_mail.html", {'usuario_receptor_mail': libro_prestado.perfil_dueno.usuario.username,
		'usuario_devolucion': libro_prestado.perfil_receptor.usuario.username, 'titulo_libro': libro_prestado.libro.titulo, 
		'autor_libro': libro_prestado.libro.titulo})

	send_mail(
			subject=titulo,
			message=mensaje_texto,
			from_email="letras.club@no-reply.com",
			recipient_list=[libro_prestado.perfil_dueno.usuario.email],
			fail_silently=True,
			html_message=html_message
		)

	return None


def mail_aceptar_prestamo(libro_prestado):
	"""
	Envía un mail al usuario que pidió el libro notificándole que sí le van a prestar el libro
	"""

	titulo = "%s ha aceptado prestarte el libro %s" % (libro_prestado.perfil_dueno.usuario.username, libro_prestado.libro.titulo)
	mensaje_texto = "%s ha aceptado prestarte el libro %s de %s, por favor visita tu perfil en Letras.Club"
	html_message = render_to_string("aceptar_prestamo_mail.html", {'usuario_receptor_mail': libro_prestado.perfil_receptor.usuario.username,
		'usuario_dueno_libro': libro_prestado.perfil_dueno.usuario.username, 'titulo_libro': libro_prestado.libro.titulo, 
		'autor_libro': libro_prestado.libro.autor, 'mensaje': libro_prestado.mensaje_aceptacion})

	send_mail(
			subject=titulo,
			message=mensaje_texto,
			from_email="letras.club@no-reply.com",
			recipient_list=[libro_prestado.perfil_receptor.usuario.email],
			fail_silently=True,
			html_message=html_message
		)

	return None
