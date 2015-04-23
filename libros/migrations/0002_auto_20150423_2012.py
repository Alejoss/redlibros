# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0001_initial'),
        ('libros', '0001_initial'),
        ('cities_light', '0003_auto_20141120_0342'),
    ]

    operations = [
        migrations.AddField(
            model_name='librosrequest',
            name='perfil_envio',
            field=models.ForeignKey(related_name='perfil_envio', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosrequest',
            name='perfil_recepcion',
            field=models.ForeignKey(related_name='perfil_recepcion', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosprestadosbibliotecacompartida',
            name='biblioteca_compartida',
            field=models.ForeignKey(to='libros.BibliotecaCompartida'),
        ),
        migrations.AddField(
            model_name='librosprestadosbibliotecacompartida',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosprestadosbibliotecacompartida',
            name='perfil_prestamo',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='perfil_dueno',
            field=models.ForeignKey(related_name='perfil_dueno', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosprestados',
            name='perfil_receptor',
            field=models.ForeignKey(related_name='perfil_receptor', to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosleidos',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosleidos',
            name='perfil',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='ciudad',
            field=models.ForeignKey(to='cities_light.City'),
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='librosdisponibles',
            name='perfil',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
        migrations.AddField(
            model_name='librosbibliotecacompartida',
            name='biblioteca_compartida',
            field=models.ForeignKey(to='libros.BibliotecaCompartida'),
        ),
        migrations.AddField(
            model_name='librosbibliotecacompartida',
            name='libro',
            field=models.ForeignKey(to='libros.Libro'),
        ),
        migrations.AddField(
            model_name='bibliotecacompartida',
            name='ciudad',
            field=models.ForeignKey(to='cities_light.City'),
        ),
        migrations.AddField(
            model_name='bibliotecacompartida',
            name='perfil_admin',
            field=models.ForeignKey(to='perfiles.Perfil'),
        ),
    ]
