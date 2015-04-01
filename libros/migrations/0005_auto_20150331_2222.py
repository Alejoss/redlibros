# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0004_librosrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosrequest',
            name='aceptado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='librosrequest',
            name='eliminado',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
