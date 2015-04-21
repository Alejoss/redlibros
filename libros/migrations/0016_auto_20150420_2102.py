# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0004_auto_20150331_2217'),
        ('libros', '0015_auto_20150420_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibrosPrestadosBibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tiempo_devolucion', models.DateTimeField(null=True)),
                ('fecha_prestamo', models.DateTimeField(null=True)),
                ('fecha_devolucion', models.DateTimeField(null=True)),
                ('biblioteca_compartida', models.ForeignKey(to='libros.BibliotecaCompartida')),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_prestamo', models.ForeignKey(to='perfiles.Perfil')),
            ],
        ),
        migrations.RemoveField(
            model_name='libroprestadosbibliotecacompartida',
            name='biblioteca_compartida',
        ),
        migrations.RemoveField(
            model_name='libroprestadosbibliotecacompartida',
            name='libro',
        ),
        migrations.RemoveField(
            model_name='libroprestadosbibliotecacompartida',
            name='perfil_prestamo',
        ),
        migrations.DeleteModel(
            name='LibroPrestadosBibliotecaCompartida',
        ),
    ]
