# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0003_auto_20141120_0342'),
        ('perfiles', '0004_auto_20150331_2217'),
        ('libros', '0007_auto_20150408_2359'),
    ]

    operations = [
        migrations.CreateModel(
            name='BibliotecaCompartida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=150, blank=True)),
                ('punto_google_maps', models.CharField(max_length=500, blank=True)),
                ('descripcion_direccion', models.CharField(max_length=500, blank=True)),
                ('hora_apertura', models.PositiveSmallIntegerField(null=True)),
                ('hora_cierre', models.PositiveSmallIntegerField(null=True)),
                ('ciudad', models.ForeignKey(to='cities_light.City')),
                ('perfil_admin', models.ForeignKey(to='perfiles.Perfil')),
            ],
        ),
        migrations.RemoveField(
            model_name='puntobiblioteca',
            name='ciudad',
        ),
        migrations.RemoveField(
            model_name='puntobiblioteca',
            name='perfil_admin',
        ),
        migrations.AlterField(
            model_name='libroprestadospunto',
            name='punto_biblioteca',
            field=models.ForeignKey(to='libros.BibliotecaCompartida'),
        ),
        migrations.AlterField(
            model_name='librospuntobiblioteca',
            name='punto_biblioteca',
            field=models.ForeignKey(to='libros.BibliotecaCompartida'),
        ),
        migrations.DeleteModel(
            name='PuntoBiblioteca',
        ),
    ]
