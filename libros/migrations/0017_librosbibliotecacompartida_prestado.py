# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0016_auto_20150420_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosbibliotecacompartida',
            name='prestado',
            field=models.BooleanField(default=False),
        ),
    ]
