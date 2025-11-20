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

    

]
