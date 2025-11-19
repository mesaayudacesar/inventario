from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:user_list')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/user_form.html', {'form': form})

@login_required
def user_update(request, pk):
    if not request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'No tienes permisos para editar usuarios.')
        return redirect('activos:home')
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Usuario actualizado exitosamente.')
        return redirect('usuarios:user_list')
    return render(request, 'usuarios/user_form.html', {'user': user})

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
