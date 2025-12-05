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
    path('crear/', views.ActivoCreateView.as_view(), name='activo-create'),
    path('<int:pk>/', views.ActivoDetailView.as_view(), name='activo_detail'),
    path('<int:pk>/editar/', views.ActivoUpdateView.as_view(), name='activo_update'),
    path('<int:pk>/eliminar/', views.ActivoDeleteView.as_view(), name='activo_delete'),
    path('eliminar-multiples/', views.eliminar_multiples_activos, name='activo_delete_multiple'),
    path('<int:pk>/historial/', views.historial_activo, name='historial_activo'),
    path('<int:pk>/trazabilidad/', views.RegistrarTrazabilidadView.as_view(), name='registrar-trazabilidad'),

    path('trazabilidad/', views.TrazabilidadListView.as_view(), name='trazabilidad'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),

    # Zonas
    path('zonas/', views.ZonaListView.as_view(), name='zona_list'),
    path('zonas/crear/', views.ZonaCreateView.as_view(), name='zona_create'),
    path('zonas/<int:pk>/editar/', views.ZonaUpdateView.as_view(), name='zona_update'),
    path('zonas/<int:pk>/eliminar/', views.ZonaDeleteView.as_view(), name='zona_delete'),

    # Categorías
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/crear/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/eliminar/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
]
