# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0002_auto_20150513_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='descripcion',
            field=models.CharField(default=' ', max_length=250, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='imagen_perfil',
            field=models.CharField(default=' ', max_length=255, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='nickname',
            field=models.CharField(default=' ', unique=True, max_length=75, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='perfil',
            name='numero_telefono_contacto',
            field=models.CharField(default=' ', max_length=55, blank=True),
            preserve_default=False,
        ),
    ]
