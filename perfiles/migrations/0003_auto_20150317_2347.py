# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0003_auto_20141120_0342'),
        ('perfiles', '0002_auto_20150317_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='ciudad',
            field=models.ForeignKey(blank=True, to='cities_light.City', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='perfil',
            name='numero_telefono_contacto',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
