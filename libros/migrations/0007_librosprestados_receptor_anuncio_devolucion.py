# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0006_librosprestados_mensaje_aceptacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosprestados',
            name='receptor_anuncio_devolucion',
            field=models.BooleanField(default=False),
        ),
    ]
