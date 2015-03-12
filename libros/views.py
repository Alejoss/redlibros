# -*- coding: utf-8 -*-

from django.shortcuts import render

from libros.models import LibrosDisponibles


def main(request):
	""" 
	Muestra un serch de libros, las últimas acciones que han tomado los usuarios en la red,
	y algo más
	"""
	template = "libros/main.html"
	
	libros = LibrosDisponibles.objects.all()
	context = {'libros':libros}
	return render(request, template, context)

def libros_ciudad(request):
	"""
	Recibe como parametro una ciudad y un pais
	"""
	template = "libros/libros_ciudad.html"
	return render(request, template)

def libro(request):
	template = "libros/libro.html"
	return render(request, template)

def libros_usuario(request):
	template = "libros/libros_usuario.html"
	return render(request, template)
