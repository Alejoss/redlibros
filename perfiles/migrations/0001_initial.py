# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=75, unique=True, null=True, blank=True)),
                ('imagen_perfil', models.CharField(max_length=255, null=True, blank=True)),
                ('descripcion', models.CharField(max_length=250, null=True, blank=True)),
                ('numero_telefono_contacto', models.IntegerField(null=True, blank=True)),
                ('actualmente_leyendo', models.ForeignKey(related_name='actualmente_leyendo', blank=True, to='libros.Libro', null=True)),
                ('ciudad', models.ForeignKey(blank=True, to='cities_light.City', null=True)),
                ('libros_leidos', models.ForeignKey(related_name='libros_leidos', blank=True, to='libros.Libro', null=True)),
                ('libros_propios', models.ForeignKey(related_name='libros_propios', blank=True, to='libros.Libro', null=True)),
                ('libros_recibidos', models.ForeignKey(related_name='libros_recibidos', blank=True, to='libros.Libro', null=True)),
                ('usuario', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
