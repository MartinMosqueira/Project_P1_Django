# Generated by Django 3.1.6 on 2021-02-19 17:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Peliculas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('duracion', models.DurationField()),
                ('descripcion', models.CharField(max_length=200)),
                ('detalle', models.CharField(max_length=100)),
                ('genero', models.CharField(max_length=20)),
                ('clasificacion', models.CharField(max_length=20)),
                ('estado', models.IntegerField(choices=[(1, 'activo'), (2, 'no activo')], default=1)),
                ('fechaComienzo', models.DateField()),
                ('fechaFinalizacion', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Salas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('estado', models.IntegerField(choices=[(1, 'habilitada'), (2, 'deshabilitada'), (3, 'eliminada')], default=1)),
                ('filas', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('asientos', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('horaProyeccion', models.TimeField()),
                ('estado', models.IntegerField(choices=[(1, 'activo'), (2, 'no activo')], default=1)),
                ('pelicula', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CinemaApp.peliculas')),
                ('sala', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CinemaApp.salas')),
            ],
        ),
        migrations.CreateModel(
            name='Butacas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('fila', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('asiento', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('proyeccion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CinemaApp.proyeccion')),
            ],
        ),
    ]
