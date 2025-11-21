from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # <-- así debe ser
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre
    

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Venta de {self.producto.nombre} - {self.cantidad}"
    

class RegistroActividad(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    accion = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Anónimo"
        return f"{usuario_str} - {self.accion} - {self.fecha:%Y-%m-%d %H:%M:%S}"
