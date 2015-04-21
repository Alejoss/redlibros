# -*- coding: utf-8 -*-
import datetime

from perfiles.models import Perfil


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

	print fecha_devolucion
	return fecha_devolucion
