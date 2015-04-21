# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0017_librosbibliotecacompartida_prestado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librosprestadosbibliotecacompartida',
            old_name='tiempo_devolucion',
            new_name='fecha_max_devolucion',
        ),
    ]
