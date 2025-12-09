from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Usuario
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import UserForm

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.rol == 'admin':
            return reverse('activos:admin_dashboard')
        elif user.rol == 'logistica':
            return reverse('activos:logistica_dashboard')
        elif user.rol == 'lectura':
            return reverse('activos:lectura_dashboard')
        elif user.rol == 'asignador':
            return reverse('activos:home')
        else:
            return reverse('activos:home')

@login_required
def user_list(request):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para ver usuarios.')
        return redirect('activos:home')
    users = Usuario.objects.all()
    return render(request, 'usuarios/user_list.html', {'users': users})

@login_required
def user_create(request):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para crear usuarios.')
        return redirect('activos:home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:user_list')
    else:
        form = UserForm()
    
    if request.GET.get('modal'):
        return render(request, 'usuarios/partials/form_user.html', {'form': form})
        
    return render(request, 'usuarios/user_form.html', {'form': form})

@login_required
def user_update(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('activos:home')
    user = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:user_list')
    else:
        form = UserForm(instance=user)
        
    if request.GET.get('modal'):
        return render(request, 'usuarios/partials/form_user.html', {'form': form})
        
    return render(request, 'usuarios/user_form.html', {'form': form})

@login_required
def user_reset_password(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para resetear contraseñas.')
        return redirect('activos:home')
    user = Usuario.objects.get(pk=pk)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Contraseña reseteada exitosamente.')
        return redirect('usuarios:user_list')
    return render(request, 'usuarios/reset_password.html', {'user': user})

@login_required
def user_toggle_active(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('activos:home')
    
    user = get_object_or_404(Usuario, pk=pk)
    
    # Evitar desactivarse a uno mismo
    if user == request.user:
        messages.error(request, 'No puedes desactivar tu propio usuario.')
        return redirect('usuarios:user_list')
        
    user.is_active = not user.is_active
    user.save()
    
    estado = "activado" if user.is_active else "desactivado"
    messages.success(request, f'Usuario {user.username} {estado} exitosamente.')
    return redirect('usuarios:user_list')

@login_required
def user_delete(request, pk):
    if request.user.rol != 'admin':
        messages.error(request, 'No tienes permisos para eliminar usuarios.')
        return redirect('activos:home')
    
    user = get_object_or_404(Usuario, pk=pk)
    
    # Evitar eliminarse a uno mismo
    if user == request.user:
        messages.error(request, 'No puedes eliminar tu propio usuario.')
        return redirect('usuarios:user_list')
        
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('usuarios:user_list')
        
    return redirect('usuarios:user_list')
