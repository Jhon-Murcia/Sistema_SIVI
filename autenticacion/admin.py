from django.contrib import admin
from .models import RegistroActividad

@admin.register(RegistroActividad)
class RegistroActividadAdmin(admin.ModelAdmin):
    list_display = ('fecha','usuario','accion')
    list_filter = ('accion','fecha','usuario')
    search_fields = ('descripcion','usuario__username','accion')
