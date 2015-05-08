# -*- coding: utf-8 -*-
from django.db import models
from django.utils.text import slugify

from cities_light.models import City
from perfiles.models import Perfil


class Libro(models.Model):
	titulo = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(null=True, blank=True)
	autor = models.CharField(max_length=255, blank=True)
	descripcion = models.TextField(null=True, blank=True, max_length=2500)

	def save(self, *args, **kwargs):
		if not self.id:
			# nuevo objecto, crear slug
			self.slug = slugify(self.titulo)

		super(Libro, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.slug


class LibrosLeidos(models.Model):
	perfil = models.ForeignKey(Perfil)
	libro = models.ForeignKey(Libro)
	fecha_lectura = models.DateTimeField(null=True)

	def __unicode__(self):
		return "Libros Leidos object: %s - %s" % (self.perfil.usuario, self.libro.titulo)


class LibrosDisponibles(models.Model):
	libro = models.ForeignKey(Libro)
	perfil = models.ForeignKey(Perfil)
	disponible = models.BooleanField(default=True)
	prestado = models.BooleanField(default=False)
	ciudad = models.ForeignKey(City)

	def __unicode__(self):
		return "Libro Disponible object: %s - %s" % (self.libro.titulo, self.perfil.usuario)


class LibrosPrestados(models.Model):
	libro = models.ForeignKey(Libro)
	perfil_dueno = models.ForeignKey(Perfil, related_name="perfil_dueno")
	perfil_receptor = models.ForeignKey(Perfil, related_name="perfil_receptor")
	fecha_max_devolucion = models.DateTimeField(null=True)
	fecha_prestamo = models.DateTimeField(null=True)
	fecha_devolucion = models.DateTimeField(null=True)

	def __unicode__(self):
		return "Libro Prestado object: %s - %s - %s" % (self.libro, self.perfil_dueno.usuario, self.perfil_receptor.usuario)


class LibrosRequest(models.Model):
	libro = models.ForeignKey(Libro)
	perfil_envio = models.ForeignKey(Perfil, related_name="perfil_envio")
	perfil_recepcion = models.ForeignKey(Perfil, related_name="perfil_recepcion")
	fecha_request = models.DateTimeField(auto_now=True)
	mensaje = models.CharField(max_length=500, blank=True)
	telefono = models.CharField(max_length=150, blank=True)
	email = models.CharField(max_length=255, blank=True)
	aceptado = models.BooleanField(default=False)
	eliminado = models.BooleanField(default=False)

	def __unicode__(self):
		return "Libro Request object: %s - %s - %s" % (self.libro.titulo, self.perfil_envio.usuario, self.perfil_recepcion.titulo)


class BibliotecaCompartida(models.Model):
	nombre = models.CharField(max_length=150, blank=True, unique=True)
	slug = models.SlugField(blank=True)
	perfil_admin = models.ForeignKey(Perfil)
	ciudad = models.ForeignKey(City)
	punto_google_maps = models.CharField(max_length=500, blank=True)
	direccion = models.CharField(max_length=500, blank=True)
	imagen = models.URLField(blank=True)
	eliminada = models.BooleanField(default=False)
	
	def save(self, *args, **kwargs):
		if not self.id:
			# nuevo objecto, crear slug
			self.slug = slugify(self.nombre)

		super(BibliotecaCompartida, self).save(*args, **kwargs)

	def __unicode__(self):
		return "Biblioteca Compartida: %s" % (self.nombre)


class LibrosBibliotecaCompartida(models.Model):
	libro = models.ForeignKey(Libro)
	biblioteca_compartida = models.ForeignKey(BibliotecaCompartida)
	disponible = models.BooleanField(default=True)
	prestado = models.BooleanField(default=False)

	def __unicode__(self):
		return "Libro BibliotecaCompartida: %s - %s" % (self.libro.titulo, self.biblioteca_compartida.nombre)


class LibrosPrestadosBibliotecaCompartida(models.Model):
	libro = models.ForeignKey(Libro)
	perfil_prestamo = models.ForeignKey(Perfil)
	biblioteca_compartida = models.ForeignKey(BibliotecaCompartida)
	fecha_max_devolucion = models.DateTimeField(null=True)
	fecha_prestamo = models.DateTimeField(null=True)
	fecha_devolucion = models.DateTimeField(null=True)

	def __unicode__(self):
		return "Libro Biblioteca Compartida: %s - %s" % (self.libro.titulo, self.biblioteca_compartida.nombre)
