# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404

from perfiles.models import Perfil


def obtener_perfil(usuario):
	return get_object_or_404(Perfil, usuario=usuario)
