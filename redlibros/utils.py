# -*- coding: utf-8 -*-
from perfiles.models import Perfil


def obtener_perfil(usuario):
	perfil, created = Perfil.objects.get_or_create(usuario=usuario)

	return perfil
