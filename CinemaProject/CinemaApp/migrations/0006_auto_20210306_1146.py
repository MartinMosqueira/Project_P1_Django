# Generated by Django 3.1.6 on 2021-03-06 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CinemaApp', '0005_butacas_estado'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='butacas',
            name='unique_butacas',
        ),
        migrations.AddConstraint(
            model_name='butacas',
            constraint=models.UniqueConstraint(fields=('proyeccion', 'fecha', 'fila', 'asiento'), name='unique_butacas'),
        ),
    ]
