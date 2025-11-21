from django.urls import path
from . import views
from pos import menu
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # --- AUTENTICACIÓN ---
    path('', views.iniciar_sesion, name='login'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.registro_view, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('invitado/', views.login_como_invitado, name='invitado'),
    
    # --- MENÚ PRINCIPAL ---
    path('menu/', menu.menu_principal, name='menu_principal'),

    # --- INVENTARIO ---
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar/', views.agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),

    # --- VENTAS ---
    path('ventas/', views.ventas, name='ventas'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),

    # --- REPORTES ---
    path('reportes/', views.report_interface_view, name='report_interface'),
    path('reportes/api/generar/', views.generate_report_api_view, name='generate_report_api'),

    # --- CONFIGURACIÓN ---
    path('configuracion/', views.config_interface_view, name='config_interface'),
    path('configuracion/perfil/', views.perfil_detail_view, name='perfil_detail'),
    path('configuracion/seguridad/', views.seguridad_settings_view, name='seguridad_settings'),
    path('configuracion/compras/', views.mis_compras_view, name='mis_compras'),
    path('configuracion/privacidad/', views.privacidad_settings_view, name='privacidad_settings'),
    path('configuracion/notificaciones/', views.notificaciones_settings_view, name='notificaciones_settings'),

    # --- SEGURIDAD (HISTORIAL) ---
    path('seguridad/', views.seguridad, name='seguridad'),
]
