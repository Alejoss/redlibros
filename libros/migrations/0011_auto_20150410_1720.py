# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0010_auto_20150410_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bibliotecacompartida',
            name='eliminada',
            field=models.BooleanField(default=False),
        ),
    ]
