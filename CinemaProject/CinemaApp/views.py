from django.shortcuts import render
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas
from django.http import JsonResponse
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from .serializers import SalasSerializer, ProyeccionesSerializer,ButacasSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from dateutil.relativedelta import * 
from collections import Counter
from itertools import islice

# Create your views here.

#ENDPOINTS PELICULAS

def get(request):
    today = date.today()
    new_date = today - relativedelta(years=1)
    peliculas=Peliculas.objects.filter(fechaComienzo__range=[new_date,today])
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
                    proyeccion_datos['sala']=proyeccion.sala.nombre
                    proyeccion_datos['fecha']=lista.date()
                    proyeccion_datos['hora']=proyeccion.horaProyeccion
                    output.append(proyeccion_datos)

        if proyeccion.estado == 2:
            return JsonResponse({'ERROR':'no hay proyecciones activas para esta pelicula'})

    if len(output) == 0:
        return JsonResponse({'ERROR':'no hay proyecciones para esta pelicula'})

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
    if len(output) == 0:
        return JsonResponse({'ERROR':'no hay proyecciones en ese rango de fecha'})

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
                    inicio=proyeccion.fechaInicio
                    fin=proyeccion.fechaFin

    if len(outputP) != 0:    
        if proyeccion.estado == 1:
            for butaca in butacas:
                if butaca.fecha >= inicio and butaca.fecha <= fin:
                    butaca_datos={}
                    butaca_datos['proyeccion']=butaca.proyeccion.id
                    butaca_datos['fecha']=butaca.fecha
                    butaca_datos['fila']=butaca.fila
                    butaca_datos['asiento']=butaca.asiento
                    butaca_datos['estado']=butaca.estado
                    outputB.append(butaca_datos)
    else:
        return JsonResponse({'ERROR':'no se encuentra una proyeccion en esa fecha'})


    return JsonResponse({'sala':outputS,'proyeccion':outputP,'butacas':outputB})

@api_view(['GET','POST',])
def proyeccion_metodos_GP(request):
    if request.method == 'GET':
        proyecciones=Proyeccion.objects.filter(estado=1)
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
        if butaca.estado == 2 or butaca.estado == 3:
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

        elif butaca.estado ==1 :
            return JsonResponse({'STATUS':'la butaca se encuentra libre'})

    return JsonResponse({"butaca":outputB,"proyeccion":outputP})
    
@api_view(['GET','POST',])
def butaca_metodos_GP(request):
    if request.method == 'GET':
        butacas=Butacas.objects.filter(estado=2)
        serializer = ButacasSerializer(butacas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer=ButacasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
def butaca_metodo_P(request,butaca_id):
    try:
        butaca = Butacas.objects.get(id=butaca_id)
    except Butacas.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = ButacasSerializer(butaca, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#ENDPOINTS REPORTES

def butacas_tiempo(request):
    today = date.today()
    new_date = today - relativedelta(month=2)
    ventas=Butacas.objects.filter(fecha__range=[new_date,today])
    output=[]
    for venta in ventas:
        venta_datos={}
        if venta.estado == 3:
            venta_datos['id']=venta.id
            venta_datos['proyeccion']=venta.proyeccion.id
            venta_datos['fecha']=venta.fecha
            venta_datos['fila']=venta.fila
            venta_datos['asiento']=venta.asiento
            venta_datos['estado']=venta.estado
            output.append(venta_datos)

    return JsonResponse({'ventas':output})

def butaca_tiempo_proyeccion(request,proyeccion_id):
    proyecciones=Proyeccion.objects.filter(id=proyeccion_id)
    today=proyecciones.values('fechaFin').first()
    today=today['fechaFin']
    new_date = today - relativedelta(days=7)
    butacas=Butacas.objects.filter(proyeccion__in=proyecciones,fecha__range=[new_date,today])

    output=[]
    outputB=[]
    for proyeccion in proyecciones:
        proyeccion_datos={}
        proyeccion_datos['id']=proyeccion.id
        proyeccion_datos['pelicula']=proyeccion.pelicula.nombre
        proyeccion_datos['sala']=proyeccion.sala.nombre
        output.append(proyeccion_datos)

    for butaca in butacas:
        butaca_datos={}
        if butaca.estado == 3:
            butaca_datos['fecha']=butaca.fecha
            butaca_datos['fila']=butaca.fila
            butaca_datos['asiento']=butaca.asiento
            butaca_datos['estado']=butaca.estado
            outputB.append(butaca_datos)

    return JsonResponse({'proyecciones':output,'ventas':outputB})

def butacas_tiempo_peliculas(request):
    peliculas=Peliculas.objects.filter(estado=1)
    butacas=Butacas.objects.filter(proyeccion__pelicula__in=peliculas)
    outputP=[]
    lista_peliculas=[]

    for butaca in butacas:
        if butaca.estado == 3:
            lista_peliculas.append(butaca.proyeccion.pelicula.nombre)
    
    for pelicula in peliculas:
        pelicula_datos={}
        veces=lista_peliculas.count(pelicula.nombre)
        pelicula_datos['pelicula']=pelicula.nombre
        pelicula_datos['ventas']=veces
        outputP.append(pelicula_datos)
    
    return JsonResponse({'ventas':outputP})

def butacas_tiempo_peliculas_ranking(request):
    today = date.today()
    new_date = today - relativedelta(years=1)
    butacas=Butacas.objects.filter(fecha__range=[new_date,today])
    list_proyecciones=[]
    output=[]

    for butaca in butacas:
        list_proyecciones.append(butaca.proyeccion.id)
    dict_proyecciones=dict(Counter(list_proyecciones).most_common(len(list_proyecciones)))
    
    for numero_id in islice(dict_proyecciones,0,5):
        proyecciones=Proyeccion.objects.filter(id=numero_id)
        for proyeccion in proyecciones:
            proyeccion_datos={}
            proyeccion_datos['nombre']=proyeccion.pelicula.nombre
            proyeccion_datos['fechaInicio']=proyeccion.fechaInicio
            proyeccion_datos['fechaFin']=proyeccion.fechaFin
            proyeccion_datos['sala']=proyeccion.sala.nombre
            proyeccion_datos['ventas']=dict_proyecciones[numero_id]
            output.append(proyeccion_datos)

    return JsonResponse({'proyecciones':output})
