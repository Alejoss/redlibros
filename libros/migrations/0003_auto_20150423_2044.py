# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_auto_20150423_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librosprestados',
            old_name='fecha_limite_devolucion',
            new_name='fecha_max_devolucion',
        ),
        migrations.RemoveField(
            model_name='librosprestados',
            name='devuelto',
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='fecha_devolucion',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='fecha_prestamo',
            field=models.DateTimeField(null=True),
        ),
    ]
