# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0003_auto_20141120_0342'),
        ('libros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='descripcion',
            field=models.TextField(max_length=2500, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='ciudad',
            field=models.ForeignKey(default=None, to='cities_light.City'),
            preserve_default=False,
        ),
    ]
