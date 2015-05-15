# -*- coding: utf-8 -*-
import datetime

from perfiles.models import Perfil
from libros.models import LibrosPrestados, LibrosPrestadosBibliotecaCompartida


# Perfil y Editar Perfil
def obtener_avatar_large(perfil):
    # Obtiene un perfil y devuelve la imagen de perfil grande.
    avatar_large = None
    if perfil.imagen_perfil is not None:
        if "facebook" in perfil.imagen_perfil:
            avatar_large = "%s?type=large" % (perfil.imagen_perfil)        
        elif "google" in perfil.imagen_perfil:
            avatar_large = (perfil.imagen_perfil).replace("sz=50", "sz=400")
        elif "puzzle" in perfil.imagen_perfil:
            avatar_large = "https://s3-us-west-1.amazonaws.com/orillalibertaria/logo_ol_puzzle_small.png"
        else:
            avatar_large = perfil.imagen_perfil
    else:
        avatar_large = "https://s3-us-west-1.amazonaws.com/orillalibertaria/tema_default.jpg"

    return avatar_large


def obtener_perfil(usuario):
	perfil, created = Perfil.objects.get_or_create(usuario=usuario)

	return perfil


def definir_fecha_devolucion(fecha_prestamo, tiempo_prestamo):
	fecha_devolucion = None
	if tiempo_prestamo == "2_semanas":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=2)
	elif tiempo_prestamo == "1_mes":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=4)
	elif tiempo_prestamo == "2_meses":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=4)		
	elif tiempo_prestamo == "3_meses":
		fecha_devolucion = fecha_prestamo + datetime.timedelta(weeks=4)
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

	perfil, creado = Perfil.objects.get_or_create(usuario=user)
	
	if backend.name == "facebook":
		print "facebook"
		imagen_url_backend = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
		print imagen_url_backend
		print "response:"
		print response
		perfil.imagen_perfil = imagen_url_backend
		perfil.save()

	elif backend.name == "google":
		print "google"
		if response['image'].get('url') is not None:
			imagen_url_backend = response['image'].get('url')
			perfil.imagen_perfil = imagen_url_backend
			perfil.save()

	return None
