# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0013_auto_20150420_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='libroprestadosbibliotecacompartida',
            name='tiempo_esperada_devolucion',
            field=models.DateTimeField(null=True),
        ),
    ]
