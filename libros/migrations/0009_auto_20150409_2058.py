# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0008_auto_20150409_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='bibliotecacompartida',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AlterField(
            model_name='bibliotecacompartida',
            name='nombre',
            field=models.CharField(unique=True, max_length=150, blank=True),
        ),
    ]
