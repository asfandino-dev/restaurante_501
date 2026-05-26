from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', views.ClienteCreateView.as_view(), name='cliente_crear'),
    path('clientes/editar/<int:pk>/', views.ClienteUpdateView.as_view(), name='cliente_editar'),
    path('clientes/eliminar/<int:pk>/', views.ClienteDeleteView.as_view(), name='cliente_eliminar'),

    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('empleados/crear/', views.EmpleadoCreateView.as_view(), name='empleado_crear'),
    path('empleados/editar/<int:pk>/', views.EmpleadoUpdateView.as_view(), name='empleado_editar'),
    path('empleados/eliminar/<int:pk>/', views.EmpleadoDeleteView.as_view(), name='empleado_eliminar'),

    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('mesas/crear/', views.MesaCreateView.as_view(), name='mesa_crear'),
    path('mesas/editar/<int:pk>/', views.MesaUpdateView.as_view(), name='mesa_editar'),
    path('mesas/eliminar/<int:pk>/', views.MesaDeleteView.as_view(), name='mesa_eliminar'),

    path('platos/', views.lista_platos, name='lista_platos'),
    path('platos/crear/', views.PlatoCreateView.as_view(), name='plato_crear'),
    path('platos/editar/<int:pk>/', views.PlatoUpdateView.as_view(), name='plato_editar'),
    path('platos/eliminar/<int:pk>/', views.PlatoDeleteView.as_view(), name='plato_eliminar'),

    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('ordenes/crear/', views.OrdenCreateView.as_view(), name='orden_crear'),
    path('ordenes/editar/<int:pk>/', views.OrdenUpdateView.as_view(), name='orden_editar'),
    path('ordenes/eliminar/<int:pk>/', views.OrdenDeleteView.as_view(), name='orden_eliminar'),

    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('facturas/crear/', views.FacturaCreateView.as_view(), name='factura_crear'),
    path('facturas/editar/<int:pk>/', views.FacturaUpdateView.as_view(), name='factura_editar'),
    path('facturas/eliminar/<int:pk>/', views.FacturaDeleteView.as_view(), name='factura_eliminar'),

    path('reporte/', views.reporte_general, name='reporte_general'),

    path('roles/', views.lista_roles, name='lista_roles'),
    path('roles/crear/', views.RolCreateView.as_view(), name='rol_crear'),
    path('roles/editar/<int:pk>/', views.RolUpdateView.as_view(), name='rol_editar'),
    path('roles/eliminar/<int:pk>/', views.RolDeleteView.as_view(), name='rol_eliminar'),

    path('permisos/', views.lista_permisos, name='lista_permisos'),
    path('permisos/crear/', views.PermisoCreateView.as_view(), name='permiso_crear'),
    path('permisos/editar/<int:pk>/', views.PermisoUpdateView.as_view(), name='permiso_editar'),
    path('permisos/eliminar/<int:pk>/', views.PermisoDeleteView.as_view(), name='permiso_eliminar'),
]