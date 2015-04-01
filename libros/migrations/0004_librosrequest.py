# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0004_auto_20150331_2217'),
        ('libros', '0003_libro_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibrosRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_request', models.DateTimeField(auto_now=True)),
                ('mensaje', models.CharField(max_length=500, blank=True)),
                ('telefono', models.CharField(max_length=150, blank=True)),
                ('libro', models.ForeignKey(to='libros.Libro')),
                ('perfil_envio', models.ForeignKey(related_name='perfil_envio', to='perfiles.Perfil')),
                ('perfil_recepcion', models.ForeignKey(related_name='perfil_recepcion', to='perfiles.Perfil')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
