# -*- coding: utf-8 -*-
from django.db import models

from cities_light.models import City
from perfiles.models import Perfil


# Create your models here.
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
