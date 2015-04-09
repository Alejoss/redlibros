# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0003_auto_20141120_0342'),
        ('perfiles', '0004_auto_20150331_2217'),
        ('libros', '0006_librosrequest_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroPrestadosPunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_prestamo', models.DateTimeField(null=True)),
                ('fecha_devolucion', models.DateTimeField(null=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_prestamo', models.ForeignKey(to='perfiles.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='LibrosPuntoBiblioteca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_dueno', models.ForeignKey(related_name='perfil_original', to='perfiles.Perfil')),
                ('perfil_tiene_actualmente', models.ForeignKey(related_name='perfil_actual', to='perfiles.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='PuntoBiblioteca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('punto_google_maps', models.CharField(max_length=500, blank=True)),
                ('descripcion_direccion', models.CharField(max_length=500, blank=True)),
                ('hora_apertura', models.PositiveSmallIntegerField(null=True)),
                ('hora_cierre', models.PositiveSmallIntegerField(null=True)),
                ('ciudad', models.ForeignKey(to='cities_light.City')),
                ('perfil_admin', models.ForeignKey(to='perfiles.Perfil')),
            ],
        ),
        migrations.AddField(
            model_name='librospuntobiblioteca',
            name='punto_biblioteca',
            field=models.ForeignKey(to='libros.PuntoBiblioteca'),
        ),
        migrations.AddField(
            model_name='libroprestadospunto',
            name='punto_biblioteca',
            field=models.ForeignKey(to='libros.PuntoBiblioteca'),
        ),
    ]
