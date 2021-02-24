from django.shortcuts import render
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas
from django.http import JsonResponse
from datetime import datetime, timedelta
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

def get_pelicula_fecha(request,nombre,rangoI,rangoF):
    rangoI=datetime.strptime(rangoI, '%Y-%m-%d')
    rangoF=datetime.strptime(rangoF, '%Y-%m-%d')
    
    lista_fechas = [rangoI + timedelta(days=d) for d in range((rangoF - rangoI).days + 1)]
    
    proyecciones=Proyeccion.objects.filter(pelicula__nombre__icontains=nombre)
    output=[]
    for proyeccion in proyecciones:
        for lista in lista_fechas:
            proyeccion_datos={}
            if lista.date() >= proyeccion.fechaInicio and lista.date() <= proyeccion.fechaFin:
                proyeccion_datos['fecha']=lista.date()
                proyeccion_datos['hora']=proyeccion.horaProyeccion
                output.append(proyeccion_datos)

    return JsonResponse({'proyecciones':output})
