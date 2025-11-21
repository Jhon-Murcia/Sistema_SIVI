from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import RegistroForm, LoginForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .models import Producto, Venta
from django.db.models import F
from .models import Venta, Producto
from django.utils import timezone
from django.urls import path
from . import views # Importa el archivo views.py de la carpeta actual
#Modulo reporte
# -------------------------------------------------------------------------
# IMPORTACIÓN CLAVE: Asumiendo que report_service.py está al mismo nivel que autenticacion/
# Si Django no encuentra 'report_service', podrías necesitar una importación relativa:
# from ..report_service import generate_report_data
# Usaré la importación que asume que es accesible desde el entorno global de Django
import report_service as report_service 
# -------------------------------------------------------------------------

# Vista 1: Renderiza la interfaz HTML (asume que reportes_interfaz.html está en 'templates/autenticacion')
# Protegemos esta vista para que solo usuarios logueados accedan al módulo de reportes.
@login_required 
def report_interface_view(request):
    """Renderiza la página que contiene la lógica de reportes."""
    # Asegúrate de que tu archivo HTML se llame 'reportes_interfaz.html' 
    # y esté en la carpeta 'templates/autenticacion' (o donde lo sirvas).
    return render(request, 'autenticacion/reportes_interfaz.html',{})


# Vista 2: El ENDPOINT de la API que el JavaScript llamará
@csrf_exempt # **IMPORTANTE:** En entornos de producción, configura el token CSRF en el JS.
             # Para pruebas, lo dejamos aquí para evitar el error 403.
@login_required 
def generate_report_api_view(request):
    """
    Recibe los filtros del frontend por POST y llama a la lógica de reportes.
    Ruta: /reportes/api/generar/
    """
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
            return JsonResponse({'error': f'Error interno del servidor: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)

#Fin modulo reportes

# ----------------------------
# LOGIN Y REGISTRO
# ----------------------------
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
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
                messages.warning(request, f"El grupo '{grupo_seleccionado}' no existe. El usuario fue creado sin grupo.")

            messages.success(request, '¡Registro exitoso! Ya puedes iniciar sesión.')
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
        return redirect('menu_principal')
    else:
        return redirect('login')


# ----------------------------
# MÓDULO DE INVENTARIO UNIFICADO
# ----------------------------
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
        Producto.objects.create(nombre=nombre, descripcion=descripcion, precio=precio, cantidad=cantidad)
        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", {
        "modo": "agregar"
    })


def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre")
        producto.descripcion = request.POST.get("descripcion")
        producto.precio = request.POST.get("precio")
        producto.cantidad = request.POST.get("cantidad")
        producto.save()
        return redirect("inventario")

    return render(request, "autenticacion/inventario.html", {
        "modo": "editar",
        "producto": producto
    })


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect("inventario")



def ventas(request):
    ventas = Venta.objects.all()
    return render(request, "autenticacion/ventas.html", {"ventas": ventas})


def agregar_venta(request):
    productos = Producto.objects.all()

    if request.method == "POST":
        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad") or 0)
        producto = get_object_or_404(Producto, id=producto_id)

        # Verificar que hay inventario suficiente
        if cantidad > producto.cantidad:
            messages.error(request, "No hay inventario suficiente para realizar la venta.")
            return redirect("agregar_venta")

        # Obtener precio unitario del producto (DecimalField)
        precio_unitario = producto.precio

        # Calcular total (precio_unitario * cantidad)
        total = precio_unitario * cantidad

        # Registrar venta incluyendo total
        Venta.objects.create(
            producto=producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            total=total
        )

        # Restar inventario
        producto.cantidad -= cantidad
        producto.save()

        messages.success(request, "Venta registrada exitosamente.")
        return redirect("ventas")

    return render(request, "autenticacion/agregar_venta.html", {"productos": productos})