from django.urls import path
from . import views
from pos import menu
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # autenticación
    path('', views.iniciar_sesion, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('login/', views.iniciar_sesion, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('invitado/', views.login_como_invitado, name='invitado'),

    # menú principal
    path('menu/', menu.menu_principal, name='menu_principal'),

    # inventario
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    path('ventas/', views.ventas, name='ventas'),
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    
    # 1. Ruta para cargar la interfaz HTML (si está en la carpeta 'templates')
    path('reportes/', views.report_interface_view, name='report_interface'),
    # 2. Ruta API para que el JavaScript llame al generar el reporte (ENDPOINT)
    path('reportes/api/generar/', views.generate_report_api_view, name='generate_report_api'),
    # 3.Ruta configuracion
    path('configuracion/', views.config_interface_view, name='config_interface'),
    # RUTAS HIJAS DEL MENÚ DE CONFIGURACIÓN:
    path('configuracion/perfil/', views.perfil_detail_view, name='perfil_detail'),
    path('configuracion/seguridad/', views.seguridad_settings_view, name='seguridad_settings'),
    path('configuracion/compras/', views.mis_compras_view, name='mis_compras'),
    path('configuracion/privacidad/', views.privacidad_settings_view, name='privacidad_settings'),
    path('configuracion/notificaciones/', views.notificaciones_settings_view, name='notificaciones_settings'),
]