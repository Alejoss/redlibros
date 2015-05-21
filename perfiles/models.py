from django.db import models
from django.contrib.auth.models import User

from cities_light.models import City


class Perfil(models.Model):
	usuario = models.OneToOneField(User, null=True)	
	imagen_perfil = models.CharField(max_length=255, blank=True)
	descripcion = models.CharField(max_length=250, blank=True)

	ciudad = models.ForeignKey(City, null=True, blank=True)
	numero_telefono_contacto = models.CharField(blank=True, max_length=55)

	libros_propios = models.ForeignKey('libros.Libro', null=True, blank=True, related_name="libros_propios")
	libros_recibidos = models.ForeignKey('libros.Libro', null=True, blank=True, related_name="libros_recibidos")

	def datos_contacto(self):

		if not self.numero_telefono_contacto and not self.usuario.email:
			return False
		else:
			datos_contacto = {'telefono': self.numero_telefono_contacto, 'email': self.usuario.email}
			return datos_contacto

	def __unicode__(self):
		return "Perfil: %s" % (self.usuario.username)
