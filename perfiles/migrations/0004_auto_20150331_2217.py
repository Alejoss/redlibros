# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0003_auto_20150317_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='actualmente_leyendo',
            field=models.ForeignKey(related_name='actualmente_leyendo', blank=True, to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='imagen_perfil',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='libros_leidos',
            field=models.ForeignKey(related_name='libros_leidos', blank=True, to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='libros_propios',
            field=models.ForeignKey(related_name='libros_propios', blank=True, to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='libros_recibidos',
            field=models.ForeignKey(related_name='libros_recibidos', blank=True, to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nickname',
            field=models.CharField(max_length=75, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
