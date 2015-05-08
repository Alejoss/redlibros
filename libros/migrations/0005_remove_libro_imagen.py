# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libros', '0004_auto_20150506_2222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='libro',
            name='imagen',
        ),
    ]
