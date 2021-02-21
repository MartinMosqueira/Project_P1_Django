from django.shortcuts import render
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.

#ENDPOINTS PELICULAS

def get(request):
    peliculas=Peliculas.objects.raw("SELECT * FROM cinemaapp_peliculas WHERE fechaComienzo BETWEEN '2020-01-01' AND '2021-01-01'")
    output=[]
    for pelicula in peliculas:
        pelicula_datos={}
        pelicula_datos['id']=pelicula.id
        pelicula_datos['nombre']=pelicula.nombre
        pelicula_datos['descripcion']=pelicula.descripcion
        output.append(pelicula_datos)

    return JsonResponse({'peliculas':output})        

def get_pelicula(request,nombre):
    peliculas=Peliculas.objects.filter(nombre=nombre)
    output=[]
    #return render(request,'peliculas.html',{'pelicula':pelicula})
    for pelicula in peliculas:
        pelicula_datos={}
        pelicula_datos['id']=pelicula.id
        pelicula_datos['nombre']=pelicula.nombre
        pelicula_datos['duracion']=pelicula.duracion
        pelicula_datos['descripcion']=pelicula.descripcion
        pelicula_datos['detalle']=pelicula.detalle
        pelicula_datos['genero']=pelicula.genero
        pelicula_datos['clasificacion']=pelicula.clasificacion
        pelicula_datos['estado']=pelicula.estado
        pelicula_datos['fechaComienzo']=pelicula.fechaComienzo
        pelicula_datos['fechaFinalizacion']=pelicula.fechaFinalizacion
        output.append(pelicula_datos)

    return JsonResponse({"pelicula":output})