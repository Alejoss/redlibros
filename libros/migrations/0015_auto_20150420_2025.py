# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0014_libroprestadosbibliotecacompartida_tiempo_esperada_devolucion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libroprestadosbibliotecacompartida',
            old_name='tiempo_esperada_devolucion',
            new_name='tiempo_devolucion',
        ),
    ]
