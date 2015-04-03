# -*- coding: utf-8 -*-
from django.contrib import admin

from libros.models import Libro, LibrosRequest

admin.site.register(Libro)
admin.site.register(LibrosRequest)
