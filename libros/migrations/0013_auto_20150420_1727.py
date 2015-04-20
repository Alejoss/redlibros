# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0012_auto_20150412_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librosbibliotecacompartida',
            name='perfil_dueno',
        ),
        migrations.RemoveField(
            model_name='librosbibliotecacompartida',
            name='perfil_tiene_actualmente',
        ),
    ]
