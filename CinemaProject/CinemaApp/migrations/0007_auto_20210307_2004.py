# Generated by Django 3.1.6 on 2021-03-07 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CinemaApp', '0006_auto_20210306_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyeccion',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CinemaApp.salas'),
        ),
    ]
