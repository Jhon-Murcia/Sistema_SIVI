from django.contrib import admin
from django.urls import path, include
from . import menu  # importa el archivo menu.py del proyecto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacion.urls')),  # para login, registro, etc.
    path('menu/', menu.menu_principal, name='menu_principal'),  # URL del menú

]
