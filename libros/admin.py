# -*- coding: utf-8 -*-
from django.contrib import admin

from libros.models import Libro, LibrosRequest, BibliotecaCompartida, LibrosBibliotecaCompartida, LibrosDisponibles

admin.site.register(Libro)
admin.site.register(LibrosRequest)
admin.site.register(BibliotecaCompartida)
admin.site.register(LibrosBibliotecaCompartida)
admin.site.register(LibrosDisponibles)
