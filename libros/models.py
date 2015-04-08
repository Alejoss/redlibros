# -*- coding: utf-8 -*-
from django.db import models

from cities_light.models import City
from perfiles.models import Perfil


class Libro(models.Model):
	titulo = models.CharField(max_length=255, blank=True)
	slug = models.SlugField(null=True, blank=True)
	autor = models.CharField(max_length=255, blank=True)
	imagen = models.CharField(max_length=255, blank=True)
	descripcion = models.TextField(null=True, blank=True, max_length=2500)


class LibrosLeidos(models.Model):
	perfil = models.ForeignKey(Perfil)
	libro = models.ForeignKey(Libro)
	fecha_lectura = models.DateTimeField(null=True)


class LibrosDisponibles(models.Model):
	libro = models.ForeignKey(Libro)
	perfil = models.ForeignKey(Perfil)
	disponible = models.BooleanField(default=True)
	ciudad = models.ForeignKey(City)


class LibrosPrestados(models.Model):
	libro = models.ForeignKey(Libro)
	perfil_dueno = models.ForeignKey(Perfil, related_name="perfil_dueno")
	perfil_receptor = models.ForeignKey(Perfil, related_name="perfil_receptor")
	fecha_limite_devolucion = models.DateTimeField(null=True)


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


class PuntoBiblioteca(models.Model):
	perfil_admin = models.ForeignKey(Perfil)
	ciudad = models.ForeignKey(City)
	punto_google_maps = models.CharField(max_length=500, blank=True)
	hora_apertura = models.PositiveSmallIntegerField(null=True)
	hora_cierre = models.PositiveSmallIntegerField(null=True)


class LibrosPuntoBiblioteca(models.Model):
	libro = models.ForeignKey(Libro)
	punto_biblioteca = models.ForeignKey(PuntoBiblioteca)
	disponible = models.BooleanField(default=True)
	perfil_dueno = models.ForeignKey(Perfil)
	perfil_tiene_actualmente = models.ForeignKey(Perfil)


class LibroPrestadosPunto(models.Model):
	libro = models.ForeignKey(Libro)
	perfil_prestamo = models.ForeignKey(Perfil)
	punto_biblioteca = models.ForeignKey(PuntoBiblioteca)
	fecha_prestamo = models.DateTimeField(null=True)
	fecha_devolucion = models.DateTimeField(null=True)
