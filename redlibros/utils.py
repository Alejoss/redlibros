# -*- coding: utf-8 -*-
import datetime

from perfiles.models import Perfil
from libros.models import LibrosPrestados, LibrosPrestadosBibliotecaCompartida


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
		imagen_url_backend = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
		perfil.imagen_perfil = imagen_url_backend
		perfil.save()
	return None
