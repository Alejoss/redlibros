from django.db import models
from django.contrib.auth.models import User


class Perfil(models.Model):
	usuario = models.OneToOneField(User, null=True)
	nickname = models.CharField(max_length=75, unique=True, null=True)
	imagen_perfil = models.CharField(max_length=255, null=True)
	descripcion = models.CharField(max_length=250, blank=True, null=True)
	# ciudad = models.ForeignKey() --> a modelo de ciudad
	actualmente_leyendo = models.ForeignKey('libros.Libro', related_name="actualmente_leyendo")
	libros_leidos = models.ForeignKey('libros.Libro', related_name="libros_leidos")
	libros_propios = models.ForeignKey('libros.Libro', related_name="libros_propios")
	libros_recibidos = models.ForeignKey('libros.Libro', related_name="libros_recibidos")
