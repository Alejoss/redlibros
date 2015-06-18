# -*- coding: utf-8 -*-
from django.contrib import admin
from django.shortcuts import redirect

from libros.models import Libro, LibrosRequest, BibliotecaCompartida, LibrosBibliotecaCompartida, LibrosDisponibles, LibrosPrestadosBibliotecaCompartida


def cambiar_dueno(modelAdmin, request, queryset):
	selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)

	request.session['libros'] = selected

	return redirect('libros:cambiar_dueno_libros')

cambiar_dueno.short_description = "Cambiar Dueno"


class LibroDisponibleAdmin(admin.ModelAdmin):

	actions = [cambiar_dueno]

admin.site.register(Libro)
admin.site.register(LibrosRequest)
admin.site.register(BibliotecaCompartida)
admin.site.register(LibrosBibliotecaCompartida)
admin.site.register(LibrosDisponibles, LibroDisponibleAdmin)
admin.site.register(LibrosPrestadosBibliotecaCompartida)
