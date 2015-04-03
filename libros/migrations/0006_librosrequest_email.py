# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0005_auto_20150331_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosrequest',
            name='email',
            field=models.CharField(max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
