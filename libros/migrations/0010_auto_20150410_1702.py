# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0009_auto_20150409_2058'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bibliotecacompartida',
            old_name='descripcion_direccion',
            new_name='direccion',
        ),
        migrations.AddField(
            model_name='bibliotecacompartida',
            name='eliminada',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bibliotecacompartida',
            name='imagen',
            field=models.URLField(blank=True),
        ),
    ]
