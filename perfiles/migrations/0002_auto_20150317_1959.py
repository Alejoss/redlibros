# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0001_initial'),
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='actualmente_leyendo',
            field=models.ForeignKey(related_name=b'actualmente_leyendo', to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='libros_leidos',
            field=models.ForeignKey(related_name=b'libros_leidos', to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='libros_propios',
            field=models.ForeignKey(related_name=b'libros_propios', to='libros.Libro', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='libros_recibidos',
            field=models.ForeignKey(related_name=b'libros_recibidos', to='libros.Libro', null=True),
            preserve_default=True,
        ),
    ]
