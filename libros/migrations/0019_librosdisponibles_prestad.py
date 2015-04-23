# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0018_auto_20150420_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosdisponibles',
            name='prestad',
            field=models.BooleanField(default=True),
        ),
    ]
