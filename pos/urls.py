from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('autenticacion.urls')),  # toda la app autenticacion maneja sus propias rutas
]
