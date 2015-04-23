# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=150, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('punto_google_maps', models.CharField(max_length=500, blank=True)),
                ('direccion', models.CharField(max_length=500, blank=True)),
                ('imagen', models.URLField(blank=True)),
                ('hora_apertura', models.PositiveSmallIntegerField(null=True)),
                ('hora_cierre', models.PositiveSmallIntegerField(null=True)),
                ('eliminada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('autor', models.CharField(max_length=255, blank=True)),
                ('imagen', models.CharField(max_length=255, blank=True)),
                ('descripcion', models.TextField(max_length=2500, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosBibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('prestado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosDisponibles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('prestado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosLeidos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_lectura', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosPrestados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_limite_devolucion', models.DateTimeField(null=True)),
                ('devuelto', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosPrestadosBibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_max_devolucion', models.DateTimeField(null=True)),
                ('fecha_prestamo', models.DateTimeField(null=True)),
                ('fecha_devolucion', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibrosRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_request', models.DateTimeField(auto_now=True)),
                ('mensaje', models.CharField(max_length=500, blank=True)),
                ('telefono', models.CharField(max_length=150, blank=True)),
                ('email', models.CharField(max_length=255, blank=True)),
                ('aceptado', models.BooleanField(default=False)),
                ('eliminado', models.BooleanField(default=False)),
                ('libro', models.ForeignKey(to='libros.Libro')),
            ],
        ),
    ]
