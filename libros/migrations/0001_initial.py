# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=255, blank=True)),
                ('autor', models.CharField(max_length=255, blank=True)),
                ('imagen', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LibrosDisponibles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('disponible', models.BooleanField(default=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil', models.ForeignKey(to='perfiles.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LibrosLeidos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_lectura', models.DateTimeField(null=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil', models.ForeignKey(to='perfiles.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LibrosPrestados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_limite_devolucion', models.DateTimeField(null=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_dueno', models.ForeignKey(related_name=b'perfil_dueno', to='perfiles.Perfil')),
                ('perfil_receptor', models.ForeignKey(related_name=b'perfil_receptor', to='perfiles.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
