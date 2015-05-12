# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    replaces = [(b'libros', '0001_initial'), (b'libros', '0002_auto_20150423_2012'), (b'libros', '0003_auto_20150423_2044'), (b'libros', '0004_auto_20150506_2222'), (b'libros', '0005_remove_libro_imagen'), (b'libros', '0006_librosprestados_mensaje_aceptacion'), (b'libros', '0007_librosprestados_receptor_anuncio_devolucion')]

    dependencies = [
        ('perfiles', '0001_initial'),
        ('cities_light', '0003_auto_20141120_0342'),
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
                ('eliminada', models.BooleanField(default=False)),
                ('ciudad', models.ForeignKey(to='cities_light.City')),
                ('perfil_admin', models.ForeignKey(to='perfiles.Perfil')),
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
                ('biblioteca_compartida', models.ForeignKey(to='libros.BibliotecaCompartida')),
            ],
        ),
        migrations.CreateModel(
            name='LibrosDisponibles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('prestado', models.BooleanField(default=False)),
                ('ciudad', models.ForeignKey(to='cities_light.City')),
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
                ('biblioteca_compartida', models.ForeignKey(to='libros.BibliotecaCompartida')),
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
                ('perfil_envio', models.ForeignKey(related_name='perfil_envio', to='perfiles.Perfil')),
                ('perfil_recepcion', models.ForeignKey(related_name='perfil_recepcion', to='perfiles.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='librosprestadosbibliotecacompartida',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosprestadosbibliotecacompartida',
            name='perfil_prestamo',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='perfil_dueno',
            field=models.ForeignKey(related_name='perfil_dueno', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='perfil_receptor',
            field=models.ForeignKey(related_name='perfil_receptor', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosleidos',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosleidos',
            name='perfil',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='perfil',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosbibliotecacompartida',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.RenameField(
            model_name='librosprestados',
            old_name='fecha_limite_devolucion',
            new_name='fecha_max_devolucion',
        ),
        migrations.RemoveField(
            model_name='librosprestados',
            name='devuelto',
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='fecha_devolucion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='fecha_prestamo',
            field=models.DateTimeField(null=True),
        ),
        migrations.RemoveField(
            model_name='libro',
            name='imagen',
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='mensaje_aceptacion',
            field=models.CharField(max_length=500, blank=True),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='receptor_anuncio_devolucion',
            field=models.BooleanField(default=False),
        ),
    ]
