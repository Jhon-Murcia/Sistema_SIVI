from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Producto, Venta, RegistroActividad
from django.db.models import F
from django.utils import timezone
from django.http import JsonResponse
import json
from django.contrib.auth import logout

# --------------------------
# MÓDULOS EXTERNOS
# --------------------------
import report_service as report_service
import config_logic as config_logic


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('login')


# ==========================
# 📊 MÓDULO DE REPORTES
# ==========================

@login_required
def report_interface_view(request):
    return render(request, 'autenticacion/reportes_interfaz.html', {})


@csrf_exempt
@login_required
def generate_report_api_view(request):
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
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            print(f"ERROR al generar reporte en Django: {e}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


# ==========================
# ⚙️ MÓDULO CONFIGURACIÓN
# ==========================

def config_interface_view(request):
    return render(request, 'autenticacion/config_interface.html', {})


def perfil_detail_view(request):
    return render(request, 'autenticacion/perfil_detail.html', {})


def seguridad_settings_view(request):
    return render(request, 'autenticacion/seguridad_settings.html', {})


def mis_compras_view(request):
    return render(request, 'autenticacion/mis_compras.html', {})


def privacidad_settings_view(request):
    return render(request, 'autenticacion/privacidad_settings.html', {})


def notificaciones_settings_view(request):
    return render(request, 'autenticacion/notificaciones_settings.html', {})



# ==========================
# 🔐 MÓDULO SEGURIDAD (AUDITORÍA)
# ==========================

@login_required
def seguridad(request):
    """
    Lista el historial completo de actividades del sistema.
    Puede filtrar por texto (usuario, acción, descripción).
    """
    query = request.GET.get("q", "")

    if query:
        registros = RegistroActividad.objects.filter(
            descripcion__icontains=query
        ) | RegistroActividad.objects.filter(
            accion__icontains=query
        ) | RegistroActividad.objects.filter(
            usuario__username__icontains=query
        )
    else:
        registros = RegistroActividad.objects.all()

    registros = registros.order_by('-fecha')

    return render(request, 'autenticacion/seguridad.html', {"registros": registros})



# ==========================
# 🔐 FUNCIÓN UNIVERSAL PARA REGISTRAR ACTIVIDADES
# ==========================

def registrar_actividad(usuario, accion, descripcion):
    """
    Registra cualquier acción del sistema en la tabla RegistroActividad.
    """
    RegistroActividad.objects.create(
        usuario=usuario,
        accion=accion,
        descripcion=descripcion,
        fecha=timezone.now()
    )



# ==========================
# 🚪 LOGIN / REGISTRO
# ==========================

def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)

            registrar_actividad(
                usuario,
                "Inicio de sesión",
                f"El usuario {usuario.username} ingresó al sistema."
            )

            return redirect('menu_principal')

        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'autenticacion/login.html', {'form': form})


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

            registrar_actividad(
                usuario,
                "Registro",
                f"Se creó el usuario {usuario.username}."
            )

            messages.success(request, '¡Registro exitoso!')
            return redirect('login')

    else:
        form = RegistroForm()

    return render(request, 'autenticacion/registro.html', {'form': form})


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

        registrar_actividad(
            invitado,
            "Inicio como invitado",
            "El usuario ingresó en modo invitado."
        )

        return redirect('menu_principal')

    return redirect('login')



# ==========================
# 📦 INVENTARIO
# ==========================

def inventario(request):
    productos = Producto.objects.all()
    return render(request, "autenticacion/inventario.html", {
        "modo": "lista",
        "productos": productos
    })


def agregar_producto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        precio = request.POST.get("precio")
        cantidad = request.POST.get("cantidad")

        p = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            cantidad=cantidad
        )

        registrar_actividad(
            request.user,
            "Agregar producto",
            f"Se agregó el producto '{p.nombre}'."
        )

        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", {"modo": "agregar"})


def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.cantidad = request.POST.get("cantidad")
        producto.save()

        registrar_actividad(
            request.user,
            "Editar producto",
            f"Se editó el producto '{producto.nombre}'."
        )

        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", {
        "modo": "editar",
        "producto": producto
    })


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    registrar_actividad(
        request.user,
        "Eliminar producto",
        f"Se eliminó el producto '{producto.nombre}'."
    )

    producto.delete()
    return redirect("inventario")



# ==========================
# 💰 VENTAS
# ==========================

def ventas(request):
    ventas = Venta.objects.all()
    return render(request, "autenticacion/ventas.html", {"ventas": ventas})


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

        Venta.objects.create(
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            total=total
        )

        producto.cantidad -= cantidad
        producto.save()

        registrar_actividad(
            request.user,
            "Registrar venta",
            f"Venta de {cantidad} unidades de '{producto.nombre}'."
        )

        messages.success(request, "Venta registrada.")
        return redirect("ventas")

    return render(request, "autenticacion/agregar_venta.html", {"productos": productos})


