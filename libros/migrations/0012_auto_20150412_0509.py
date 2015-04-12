# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0004_auto_20150331_2217'),
        ('libros', '0011_auto_20150410_1720'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroPrestadosBibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_prestamo', models.DateTimeField(null=True)),
                ('fecha_devolucion', models.DateTimeField(null=True)),
                ('biblioteca_compartida', models.ForeignKey(to='libros.BibliotecaCompartida')),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_prestamo', models.ForeignKey(to='perfiles.Perfil')),
            ],
        ),
        migrations.CreateModel(
            name='LibrosBibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('biblioteca_compartida', models.ForeignKey(to='libros.BibliotecaCompartida')),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_dueno', models.ForeignKey(related_name='perfil_original', to='perfiles.Perfil')),
                ('perfil_tiene_actualmente', models.ForeignKey(related_name='perfil_actual', to='perfiles.Perfil')),
            ],
        ),
        migrations.RemoveField(
            model_name='libroprestadospunto',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='libroprestadospunto',
            name='perfil_prestamo',
        ),
        migrations.RemoveField(
            model_name='libroprestadospunto',
            name='punto_biblioteca',
        ),
        migrations.RemoveField(
            model_name='librospuntobiblioteca',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='librospuntobiblioteca',
            name='perfil_dueno',
        ),
        migrations.RemoveField(
            model_name='librospuntobiblioteca',
            name='perfil_tiene_actualmente',
        ),
        migrations.RemoveField(
            model_name='librospuntobiblioteca',
            name='punto_biblioteca',
        ),
        migrations.DeleteModel(
            name='LibroPrestadosPunto',
        ),
        migrations.DeleteModel(
            name='LibrosPuntoBiblioteca',
        ),
    ]
