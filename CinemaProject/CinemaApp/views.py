from django.shortcuts import render
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from .serializers import SalasSerializer, ProyeccionesSerializer
from rest_framework.response import Response
from rest_framework import status

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
        if proyeccion.estado == 1:
            for lista in lista_fechas:
                proyeccion_datos={}
                if lista.date() >= proyeccion.fechaInicio and lista.date() <= proyeccion.fechaFin:
                    proyeccion_datos['fecha']=lista.date()
                    proyeccion_datos['hora']=proyeccion.horaProyeccion
                    output.append(proyeccion_datos)

    return JsonResponse({'proyecciones':output})

#ENDPOINTS SALAS

def get_sala_nombre(request,nombre):
    salas=Salas.objects.filter(nombre=nombre)
    output=[]
    for sala in salas:
        sala_datos={}
        sala_datos['id']=sala.id
        sala_datos['nombre']=sala.nombre
        sala_datos['estado']=sala.estado
        sala_datos['filas']=sala.filas
        sala_datos['asientos']=sala.asientos
        output.append(sala_datos)

    return JsonResponse({'sala':output})

@api_view(['GET','POST',])
def sala_metodos_GP(request):
    if request.method == 'GET':
        salas=Salas.objects.all()
        serializer = SalasSerializer(salas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer=SalasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT','DELETE',])
def sala_metodos_PD(request,sala_id):
    try:
        salas = Salas.objects.get(id=sala_id)
    except Salas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = SalasSerializer(salas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if salas.estado == 3:
            salas.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('ERROR: No se puede eliminar sala')

#ENDPOINTS PROYECCION

def get_proyeccion_fecha_rango(request,rangoI,rangoF):
    rangoI=datetime.strptime(rangoI, '%Y-%m-%d')
    rangoF=datetime.strptime(rangoF, '%Y-%m-%d')

    lista_fechas = [rangoI + timedelta(days=d) for d in range((rangoF - rangoI).days + 1)]

    proyecciones=Proyeccion.objects.all()
    output=[]
    for proyeccion in proyecciones:
        if proyeccion.estado == 1:
            for lista in lista_fechas:
                proyeccion_datos={}
                if lista.date() >= proyeccion.fechaInicio and lista.date() <= proyeccion.fechaFin:
                    proyeccion_datos['sala']=proyeccion.sala.nombre
                    proyeccion_datos['pelicula']=proyeccion.pelicula.nombre
                    proyeccion_datos['fecha']=lista.date()
                    proyeccion_datos['hora']=proyeccion.horaProyeccion
                    output.append(proyeccion_datos)
             
    return JsonResponse({'proyecciones':output})

def get_proyeccion_fecha(request,nombre,fecha):
    fecha=datetime.strptime(fecha, '%Y-%m-%d')
    proyecciones=Proyeccion.objects.filter(pelicula__nombre__icontains=nombre)
    butacas=Butacas.objects.filter(proyeccion__in=proyecciones)
    outputP=[]
    outputS=[]
    outputB=[]
    for proyeccion in proyecciones:
        if proyeccion.estado == 1:
            proyeccion_datos={}
            sala_datos={}
            if fecha.date() >= proyeccion.fechaInicio and fecha.date() <= proyeccion.fechaFin:
                    sala_datos['nombre']=proyeccion.sala.nombre
                    sala_datos['estado']=proyeccion.sala.estado
                    sala_datos['filas']=proyeccion.sala.filas
                    sala_datos['asientos']=proyeccion.sala.asientos
                    proyeccion_datos['pelicula']=proyeccion.pelicula.nombre
                    proyeccion_datos['fecha']=fecha
                    proyeccion_datos['hora']=proyeccion.horaProyeccion
                    outputS.append(sala_datos)
                    outputP.append(proyeccion_datos)
    
    for butaca in butacas:
        butaca_datos={}
        butaca_datos['fecha']=butaca.fecha
        butaca_datos['fila']=butaca.fila
        butaca_datos['asiento']=butaca.asiento
        butaca_datos['estado']=butaca.estado
        outputB.append(butaca_datos)


    return JsonResponse({'sala':outputS,'proyeccion':outputP,'butacas':outputB})

@api_view(['GET','POST',])
def proyeccion_metodos_GP(request):
    if request.method == 'GET':
        proyecciones=Proyeccion.objects.all()
        serializer = ProyeccionesSerializer(proyecciones, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer=ProyeccionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
def proyeccion_metodo_P(request, proyeccion_id):
    try:
        proyeccion = Proyeccion.objects.get(id=proyeccion_id)
    except Proyeccion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = ProyeccionesSerializer(proyeccion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ENDPOINTS BUTACAS

def get_butaca(request,proyeccion,fecha,fila,asiento):
    butacas=Butacas.objects.filter(proyeccion__pelicula__nombre__icontains=proyeccion,fecha=fecha,fila=fila,asiento=asiento)
    outputB=[]
    outputP=[]
    for butaca in butacas:
        butaca_datos={}
        proyeccion_datos={}
        butaca_datos['id']=butaca.id
        proyeccion_datos['pelicula']=butaca.proyeccion.pelicula.nombre
        proyeccion_datos['sala']=butaca.proyeccion.sala.nombre
        proyeccion_datos['fechaInicio']=butaca.proyeccion.fechaInicio
        proyeccion_datos['fechaFin']=butaca.proyeccion.fechaFin
        butaca_datos['fecha']=butaca.fecha
        butaca_datos['fila']=butaca.fila
        butaca_datos['asiento']=butaca.asiento
        butaca_datos['estado']=butaca.estado
        outputB.append(butaca_datos)
        outputP.append(proyeccion_datos)

    return JsonResponse({"butaca":outputB,"proyeccion":outputP})