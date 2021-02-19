from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

seleccion_estado=[(1,'activo'),(2,'no activo')]
seleccion_estado_salas=[(1,'habilitada'),(2,'deshabilitada'),(3,'eliminada')]

class Peliculas(models.Model):
    nombre=models.CharField(max_length=50)
    duracion=models.DurationField()
    descripcion=models.CharField(max_length=200)
    detalle=models.CharField(max_length=100)
    genero=models.CharField(max_length=20)
    clasificacion=models.CharField(max_length=20)
    estado=models.IntegerField(null=False,blank=False,choices=seleccion_estado,default=1)
    fechaComienzo=models.DateField()
    fechaFinalizacion=models.DateField()

class Salas(models.Model):
    nombre=models.CharField(max_length=20)
    estado=models.IntegerField(null=False,blank=False,choices=seleccion_estado_salas,default=1)
    filas=models.IntegerField(validators=[MinValueValidator(1)])
    asientos=models.IntegerField(validators=[MinValueValidator(1)])

class Proyeccion(models.Model):
    sala=models.OneToOneField(Salas, null=False, blank=False, on_delete=models.CASCADE)
    pelicula=models.OneToOneField(Peliculas, null=False, blank=False, on_delete=models.CASCADE)
    fechaInicio=models.DateField()
    fechaFin=models.DateField()
    horaProyeccion=models.TimeField()
    estado=models.IntegerField(null=False,blank=False,choices=seleccion_estado,default=1)

class Butacas(models.Model):
    proyeccion=models.ForeignKey(Proyeccion, null=False, blank=False, on_delete=models.CASCADE)
    fecha=models.DateField()
    fila=models.IntegerField(validators=[MinValueValidator(1)])
    asiento=models.IntegerField(validators=[MinValueValidator(1)])
