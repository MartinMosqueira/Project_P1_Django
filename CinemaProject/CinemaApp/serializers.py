from rest_framework import serializers
from .models import Salas, Proyeccion

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
    