# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0005_remove_libro_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosprestados',
            name='mensaje_aceptacion',
            field=models.CharField(max_length=500, blank=True),
        ),
    ]
