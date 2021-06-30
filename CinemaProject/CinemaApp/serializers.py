from rest_framework import serializers
from .models import Salas, Proyeccion, Butacas, Peliculas

class SalasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Salas
        fields='__all__'

class ProyeccionesSerializer(serializers.ModelSerializer):
    sala=serializers.SlugRelatedField(queryset = Salas.objects.all(), slug_field ='nombre')
    pelicula=serializers.SlugRelatedField(queryset = Peliculas.objects.all() ,slug_field ='nombre')
    #sala=serializers.CharField(source='sala.nombre')
    #pelicula=serializers.CharField(source='pelicula.nombre')
    class Meta:
        model=Proyeccion
        fields=['id','sala','pelicula','fechaInicio','fechaFin','horaProyeccion','estado']
    
    def create(self, validated_data):
        return Proyeccion.objects.create(**validated_data)

class ButacasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Butacas
        fields='__all__'
    