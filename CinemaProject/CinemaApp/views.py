from django.shortcuts import render
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas

# Create your views here.

def get(request):
    #peliculas=Peliculas.objects.all()
    peliculas=Peliculas.objects.raw("SELECT * FROM cinemaapp_peliculas WHERE fechaComienzo BETWEEN '2020-01-01' AND '2021-01-01'")
    return render(request,'peliculas.html',{'pelicula':peliculas})
