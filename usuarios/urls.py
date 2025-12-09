from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/crear/', views.user_create, name='user_create'),
    path('usuarios/<int:pk>/editar/', views.user_update, name='user_update'),
    path('usuarios/<int:pk>/reset-password/', views.user_reset_password, name='user_reset_password'),
    path('usuarios/<int:pk>/toggle-active/', views.user_toggle_active, name='user_toggle_active'),
    path('usuarios/<int:pk>/eliminar/', views.user_delete, name='user_delete'),
]
