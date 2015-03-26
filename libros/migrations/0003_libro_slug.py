# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0002_auto_20150317_2347'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
