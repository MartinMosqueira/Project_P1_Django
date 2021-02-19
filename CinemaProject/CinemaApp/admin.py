from django.contrib import admin
from CinemaApp.models import Peliculas, Salas, Proyeccion, Butacas

# Register your models here.

class PeliculasAdmin(admin.ModelAdmin):
    list_display=('nombre','duracion','descripcion','detalle','genero','clasificacion','estado','fechaComienzo','fechaFinalizacion')
class SalasAdmin(admin.ModelAdmin):
    list_display=('nombre','estado','filas','asientos')

admin.site.register(Peliculas, PeliculasAdmin)
admin.site.register(Salas,SalasAdmin)
admin.site.register(Proyeccion)
admin.site.register(Butacas)
