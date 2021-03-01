"""CinemaProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from CinemaApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pelicula/',views.get),
    path('pelicula/<str:nombre>/',views.get_pelicula),
    path('pelicula/<str:nombre>/<str:rangoI>/<str:rangoF>',views.get_pelicula_fecha),
    path('sala/<str:nombre>',views.get_sala_nombre),
    path('salas/',views.sala_metodos_GP),
    path('salas/<int:sala_id>',views.sala_metodos_PD),
    path('proyeccion/fecha/<str:rangoI>/<str:rangoF>',views.get_proyeccion_fecha_rango),
    path('proyeccion/pelicula/<str:nombre>/<str:fecha>',views.get_proyeccion_fecha),
    path('proyeccion/',views.proyeccion_metodos_GP),
    path('proyeccion/<str:proyeccion_id>',views.proyeccion_metodo_P),
    path('butaca/<str:proyeccion>/<str:fecha>/<int:fila>/<int:asiento>',views.get_butaca)
]
