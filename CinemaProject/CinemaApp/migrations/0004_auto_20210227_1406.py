# Generated by Django 3.1.6 on 2021-02-27 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CinemaApp', '0003_auto_20210223_1856'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='butacas',
            constraint=models.UniqueConstraint(fields=('proyeccion', 'fila', 'asiento'), name='unique_butacas'),
        ),
        migrations.AlterModelTable(
            name='butacas',
            table='app_butacas',
        ),
    ]
