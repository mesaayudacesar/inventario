from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import UserForm

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        user_groups = user.groups.values_list('name', flat=True)
        if user.is_superuser or 'Admin' in user_groups:
            return reverse('activos:admin_dashboard')
        elif 'Logística' in user_groups:
            return reverse('activos:logistica_dashboard')
        elif 'Lectura' in user_groups:
            return reverse('activos:lectura_dashboard')
        else:
            return reverse('activos:home')

@login_required
def user_list(request):
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'No tienes permisos para ver usuarios.')
        return redirect('activos:home')
    users = User.objects.all()
    return render(request, 'usuarios/user_list.html', {'users': users})

@login_required
def user_create(request):
    if not request.user.groups.filter(name='Admin').exists():
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
    return render(request, 'usuarios/user_form.html', {'form': form})

@login_required
def user_update(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('activos:home')
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'usuarios/user_form.html', {'form': form})

@login_required
def user_reset_password(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'No tienes permisos para resetear contraseñas.')
        return redirect('activos:home')
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user.set_password(new_password)
        user.save()
        messages.success(request, 'Contraseña reseteada exitosamente.')
        return redirect('usuarios:user_list')
    return render(request, 'usuarios/reset_password.html', {'user': user})
