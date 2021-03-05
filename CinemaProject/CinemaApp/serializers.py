from rest_framework import serializers
from .models import Salas, Proyeccion, Butacas

class SalasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Salas
        fields='__all__'

class ProyeccionesSerializer(serializers.ModelSerializer):
    sala=serializers.CharField(source='sala.nombre')
    pelicula=serializers.CharField(source='pelicula.nombre')
    class Meta:
        model=Proyeccion
        fields=['id','sala','pelicula','fechaInicio','fechaFin','horaProyeccion','estado']

class ButacasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Butacas
        fields='__all__'
    