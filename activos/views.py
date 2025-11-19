from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from django.contrib.auth.models import Group
from django.db import models
from django.contrib import messages
from .models import Activo, Movimiento, Ubicacion, Categoria, Historial

@login_required
def dashboard_redirect(request):
    user_groups = request.user.groups.values_list('name', flat=True)
    if 'Admin' in user_groups:
        return redirect(reverse('activos:admin_dashboard'))
    elif 'Logística' in user_groups:
        return redirect(reverse('activos:logistica_dashboard'))
    elif 'Lectura' in user_groups:
        return redirect(reverse('activos:lectura_dashboard'))
    else:
        return redirect(reverse('activos:home'))

@login_required
def admin_dashboard(request):
    if not request.user.groups.filter(name='Admin').exists():
        return redirect('activos:home')
    total_activos = Activo.objects.count()
    asignados = Activo.objects.filter(estado__icontains='asignado').count()
    en_bodega = Activo.objects.filter(estado__icontains='bodega').count()
    dados_baja = Activo.objects.filter(estado__icontains='baja').count()
    return render(request, 'activos/admin_dashboard.html', {
        'total_activos': total_activos,
        'asignados': asignados,
        'en_bodega': en_bodega,
        'dados_baja': dados_baja,
    })

@login_required
def logistica_dashboard(request):
    if not request.user.groups.filter(name='Logística').exists():
        return redirect('activos:home')
    activos_por_estado = Activo.objects.values('estado').annotate(count=models.Count('estado'))
    movimientos_recientes = Movimiento.objects.order_by('-fecha')[:10]
    return render(request, 'activos/logistica_dashboard.html', {
        'activos_por_estado': activos_por_estado,
        'movimientos_recientes': movimientos_recientes,
    })

@login_required
def lectura_dashboard(request):
    if not request.user.groups.filter(name='Lectura').exists():
        return redirect('activos:home')
    total_activos = Activo.objects.count()
    return render(request, 'activos/lectura_dashboard.html', {
        'total_activos': total_activos,
    })

class ActivoListView(LoginRequiredMixin, ListView):
    model = Activo
    template_name = 'activos/home.html'
    context_object_name = 'activos'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(name='Admin').exists():
            return redirect('activos:admin_dashboard')
        return super().get(request, *args, **kwargs)


@login_required
def exportar_excel(request):
    activos = Activo.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario de Activos"

    # Headers
    headers = [field.name for field in Activo._meta.get_fields()]
    ws.append(headers)

    # Data
    for activo in activos:
        row = []
        for field in headers:
            row.append(str(getattr(activo, field)))
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventario_activos.xlsx'
    wb.save(response)
    return response

class ActivoCreateView(LoginRequiredMixin, CreateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

class ActivoDetailView(LoginRequiredMixin, DetailView):
    model = Activo
    template_name = 'activos/activo_detail.html'

class ActivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

class ActivoDeleteView(LoginRequiredMixin, DeleteView):
    model = Activo
    template_name = 'activos/activo_confirm_delete.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Ubicacion CRUD
class UbicacionListView(LoginRequiredMixin, ListView):
    model = Ubicacion
    template_name = 'activos/ubicacion_list.html'
    context_object_name = 'ubicaciones'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver ubicaciones.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class UbicacionCreateView(LoginRequiredMixin, CreateView):
    model = Ubicacion
    fields = ['nombre', 'descripcion']
    template_name = 'activos/ubicacion_form.html'
    success_url = reverse_lazy('activos:ubicacion_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear ubicaciones.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class UbicacionUpdateView(LoginRequiredMixin, UpdateView):
    model = Ubicacion
    fields = ['nombre', 'descripcion']
    template_name = 'activos/ubicacion_form.html'
    success_url = reverse_lazy('activos:ubicacion_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar ubicaciones.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class UbicacionDeleteView(LoginRequiredMixin, DeleteView):
    model = Ubicacion
    template_name = 'activos/ubicacion_confirm_delete.html'
    success_url = reverse_lazy('activos:ubicacion_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar ubicaciones.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Categoria CRUD
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'activos/categoria_list.html'
    context_object_name = 'categorias'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'activos/categoria_form.html'
    success_url = reverse_lazy('activos:categorias')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = ['nombre', 'descripcion']
    template_name = 'activos/categoria_form.html'
    success_url = reverse_lazy('activos:categorias')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'activos/categoria_confirm_delete.html'
    success_url = reverse_lazy('activos:categorias')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Movimiento CRUD
class MovimientoListView(LoginRequiredMixin, ListView):
    model = Movimiento
    template_name = 'activos/movimiento_list.html'
    context_object_name = 'movimientos'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para ver movimientos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Movimiento registration
class RegistrarMovimientoView(LoginRequiredMixin, CreateView):
    model = Movimiento
    fields = ['tipo', 'ubicacion_origen', 'ubicacion_destino', 'estado_nuevo', 'descripcion']
    template_name = 'activos/registrar_movimiento.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para registrar movimientos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activo'] = get_object_or_404(Activo, pk=self.kwargs['pk'])
        context['ubicaciones'] = Ubicacion.objects.all()
        return context

    def form_valid(self, form):
        activo = get_object_or_404(Activo, pk=self.kwargs['pk'])
        form.instance.activo = activo
        form.instance.usuario = self.request.user
        form.instance.estado_anterior = activo.estado

        if form.cleaned_data['estado_nuevo']:
            activo.estado = form.cleaned_data['estado_nuevo']
            activo.save()

        if form.cleaned_data['ubicacion_destino']:
            activo.ubicacion = form.cleaned_data['ubicacion_destino']
            activo.save()

        messages.success(self.request, 'Movimiento registrado exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('activos:activo_detail', kwargs={'pk': self.kwargs['pk']})


# Historial de activo
@login_required
def historial_activo(request, pk):
    activo = get_object_or_404(Activo, pk=pk)
    historial = Historial.objects.filter(activo=activo).order_by('-fecha')
    movimientos = Movimiento.objects.filter(activo=activo).order_by('-fecha')
    return render(request, 'activos/historial_activo.html', {
        'activo': activo,
        'historial': historial,
        'movimientos': movimientos,
    })

# Reporte por sede
@login_required
def reporte_por_sede(request):
    if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
        messages.error(request, 'No tienes permisos para ver reportes.')
        return redirect('activos:home')

    sede_id = request.GET.get('sede')
    if sede_id:
        sede = get_object_or_404(Ubicacion, id=sede_id)
        activos = Activo.objects.filter(ubicacion=sede)
    else:
        activos = Activo.objects.all()
        sede = None

    sedes = Ubicacion.objects.all()
    return render(request, 'activos/reporte_por_sede.html', {
        'activos': activos,
        'sedes': sedes,
        'sede_seleccionada': sede,
    })

@login_required
def exportar_csv(request):
    activos = Activo.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=inventario_activos.csv'
    writer = csv.writer(response)
    writer.writerow([field.name for field in Activo._meta.get_fields()])
    for activo in activos:
        writer.writerow([str(getattr(activo, field.name)) for field in Activo._meta.get_fields()])
    return response

# Update ActivoUpdateView for permissions
class ActivoUpdateView(LoginRequiredMixin, UpdateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para editar activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Update ActivoCreateView for permissions
class ActivoCreateView(LoginRequiredMixin, CreateView):
    model = Activo
    fields = '__all__'
    template_name = 'activos/activo_form.html'
    success_url = reverse_lazy('activos:home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear activos.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

