import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from .models import Producto, Venta
from django.db.models import F
from django.utils import timezone
# from django.urls import path
# from . import views # Importa el archivo views.py de la carpeta actual#Modulo reporte
# -------------------------------------------------------------------------
# IMPORTACIÓN CLAVE: Asumiendo que report_service.py está al mismo nivel que autenticacion/
# Si Django no encuentra 'report_service', podrías necesitar una importación relativa:
# from ..report_service import generate_report_data
# Usaré la importación que asume que es accesible desde el entorno global de Django
import report_service as report_service 
import config_logic as config_logic
=======
from django.http import JsonResponse

from django.db import transaction
from django.utils import timezone
>>>>>>> 368006431b845973f221dfdfc0fbf8c994d0067d

# Modelos
from .models import Producto, Venta, RegistroActividad

# Formularios
from .forms import RegistroForm, LoginForm

# Módulo de reportes
import report_service


# -------------------------------------------------------------------
# MODULO DE REPORTES
# -------------------------------------------------------------------

@login_required
def report_interface_view(request):
    """Interfaz HTML del módulo de reportes"""
    return render(request, 'autenticacion/reportes_interfaz.html', {})


@csrf_exempt
@login_required
def generate_report_api_view(request):
    """API que recibe filtros y genera reportes"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            filters = {
                'reportType': data.get('reportType'),
                'startDate': data.get('startDate'),
                'endDate': data.get('endDate'),
                'userId': data.get('userId', ''),
                'category': data.get('category', ''),
            }

            report_data = report_service.generate_report_data(filters)
            return JsonResponse(report_data)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

        except Exception as e:
            print(f"ERROR ▶ {e}")
            return JsonResponse({'error': f'Error interno: {e}'}, status=500)

    return JsonResponse({'error': 'Usa POST'}, status=405)



# -------------------------------------------------------------------
# LOGIN / REGISTRO
# -------------------------------------------------------------------

<<<<<<< HEAD

#Inicio modulo configuracion
# En autenticacion/views.py

from django.shortcuts import render
# ... otras importaciones ...

def config_interface_view(request):
    """
    Vista principal que renderiza el menú de configuración.
    """
    # En un proyecto real, pasarías el user_id o el objeto de usuario aquí
    context = {}
    return render(request, 'autenticacion/config_interface.html', context)

# En autenticacion/views.py

# Asegúrate de importar tu lógica de configuración
import config_logic

def perfil_detail_view(request):
    """Vista para ver y editar los datos personales del usuario."""
    # Aquí puedes llamar a config_logic.obtener_datos_perfil(request.user.id)
    return render(request, 'autenticacion/perfil_detail.html', {})

def seguridad_settings_view(request):
    """Vista para cambiar la contraseña y otros ajustes de seguridad."""
    return render(request, 'autenticacion/seguridad_settings.html', {})

def mis_compras_view(request):
    """Vista para mostrar el historial de compras del usuario."""
    # Si este módulo está en otra app (ej. 'ventas'), debes enlazarlo allí.
    # Por ahora, lo dejamos aquí para que compile.
    return render(request, 'autenticacion/mis_compras.html', {})

def privacidad_settings_view(request):
    """Vista para configurar las opciones de privacidad."""
    return render(request, 'autenticacion/privacidad_settings.html', {})

def notificaciones_settings_view(request):
    """Vista para configurar las opciones de notificaciones."""
    return render(request, 'autenticacion/notificaciones_settings.html', {})


#Fin modulo configuracion



# ----------------------------
# LOGIN Y REGISTRO
# ----------------------------
=======
>>>>>>> 368006431b845973f221dfdfc0fbf8c994d0067d
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            # Registrar actividad
            RegistroActividad.objects.create(
                usuario=usuario,
                accion="Inicio de sesión",
                descripcion=f"Inicio de sesión exitoso."
            )

            return redirect('menu_principal')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, "autenticacion/login.html", {'form': form})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            grupo_seleccionado = form.cleaned_data.get('grupo')

            try:
                grupo = Group.objects.get(name=grupo_seleccionado)
                usuario.groups.add(grupo)
            except Group.DoesNotExist:
                messages.warning(request, f"El grupo '{grupo_seleccionado}' no existe.")

            messages.success(request, "Registro exitoso.")
            return redirect('login')

    else:
        form = RegistroForm()

    return render(request, "autenticacion/registro.html", {'form': form})


@login_required
def dashboard(request):
    return render(request, 'autenticacion/dashboard.html')


def login_como_invitado(request):
    if request.method == 'POST':
        invitado, creado = User.objects.get_or_create(username='invitado')
        if creado:
            invitado.set_password('invitado1234')
            invitado.save()

        login(request, invitado)

        RegistroActividad.objects.create(
            usuario=invitado,
            accion="Inicio de sesión",
            descripcion="Inicio como invitado"
        )

        return redirect('menu_principal')

    return redirect('login')



# -------------------------------------------------------------------
# INVENTARIO (VERSIÓN UNIFICADA)
# -------------------------------------------------------------------

@login_required
def inventario(request):
    productos = Producto.objects.all()
    return render(request, "autenticacion/inventario.html", {
        "modo": "lista",
        "productos": productos
    })


@login_required
def agregar_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        cantidad = request.POST.get("cantidad")

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad
        )

        # Auditoría
        RegistroActividad.objects.create(
            usuario=request.user,
            accion="Producto agregado",
            descripcion=f"Agregó '{nombre}', cantidad={cantidad}, precio={precio}"
        )

        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", { "modo": "agregar" })


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.cantidad = request.POST.get("cantidad")
        producto.save()

        # Auditoría
        RegistroActividad.objects.create(
            usuario=request.user,
            accion="Producto editado",
            descripcion=f"Editó producto {producto.nombre} (ID {producto.id})"
        )

        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", {
        "modo": "editar",
        "producto": producto
    })


@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    nombre = producto.nombre

    producto.delete()

    RegistroActividad.objects.create(
        usuario=request.user,
        accion="Producto eliminado",
        descripcion=f"Eliminó '{nombre}'"
    )

    return redirect("inventario")



# -------------------------------------------------------------------
# VENTAS
# -------------------------------------------------------------------

@login_required
def ventas(request):
    ventas = Venta.objects.all()
    return render(request, "autenticacion/ventas.html", {"ventas": ventas})


@login_required
def agregar_venta(request):
    productos = Producto.objects.all()

    if request.method == "POST":
        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad") or 0)
        producto = get_object_or_404(Producto, id=producto_id)

        if cantidad > producto.cantidad:
            messages.error(request, "Inventario insuficiente.")
            return redirect("agregar_venta")

        precio_unitario = producto.precio
        total = precio_unitario * cantidad

        with transaction.atomic():
            Venta.objects.create(
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                total=total
            )

            producto.cantidad -= cantidad
            producto.save()

        # Auditoría
        RegistroActividad.objects.create(
            usuario=request.user,
            accion="Venta registrada",
            descripcion=f"{cantidad}x {producto.nombre} — total {total}"
        )

        messages.success(request, "Venta registrada correctamente.")
        return redirect("ventas")

    return render(request, "autenticacion/agregar_venta.html", {"productos": productos})



# -------------------------------------------------------------------
# SEGURIDAD: HISTORIAL DE ACTIVIDADES
# -------------------------------------------------------------------

@login_required
def seguridad(request):
    registros = RegistroActividad.objects.all().order_by('-fecha')
    return render(request, 'autenticacion/seguridad.html', {"registros": registros})
