from django.urls import path
from . import views

app_name = 'activos'

urlpatterns = [
    path('', views.ActivoListView.as_view(), name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logistica-dashboard/', views.logistica_dashboard, name='logistica_dashboard'),
    path('lectura-dashboard/', views.lectura_dashboard, name='lectura_dashboard'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('reporte-por-sede/', views.reporte_por_sede, name='reporte_por_sede'),
    path('activos/crear/', views.ActivoCreateView.as_view(), name='activo-create'),
    path('activos/<int:pk>/', views.ActivoDetailView.as_view(), name='activo_detail'),
    path('activos/<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='activo_update'),
    path('activos/<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='activo_delete'),
    path('activos/<int:pk>/historial/', views.historial_activo, name='historial_activo'),
    path('activos/<int:pk>/movimiento/', views.RegistrarMovimientoView.as_view(), name='registrar-movimiento'),
    path('ubicaciones/', views.UbicacionListView.as_view(), name='ubicacion_list'),
    path('ubicaciones/crear/', views.UbicacionCreateView.as_view(), name='ubicacion-create'),
    path('ubicaciones/<int:pk>/editar/', views.UbicacionUpdateView.as_view(), name='ubicacion-update'),
    path('ubicaciones/<int:pk>/eliminar/', views.UbicacionDeleteView.as_view(), name='ubicacion-delete'),
    path('categorias/', views.CategoriaListView.as_view(), name='categorias'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria-delete'),
    path('movimientos/', views.MovimientoListView.as_view(), name='movimientos'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
]
