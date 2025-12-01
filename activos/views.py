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
from .models import Activo, Trazabilidad, Historial, Zona, Categoria

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
    movimientos_recientes = Trazabilidad.objects.order_by('-fecha')[:10]
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


@login_required
def exportar_excel(request):
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    
    activos = Activo.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario de Activos"

    # Definir estilos
    header_fill = PatternFill(start_color="0F172A", end_color="0F172A", fill_type="solid")
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    # Headers
    headers = ['ITEM', 'DOCUMENTO', 'NOMBRES Y APELLIDOS', 'IMEI 1', 'IMEI 2', 'S/N', 
               'MAC SUPERFLEX', 'MARCA', 'ACTIVO', 'CARGO', 'ESTADO', 'FECHA CONFIRMACIÓN',
               'RESPONSABLE', 'IDENTIFICACIÓN', 'ZONA', 'CATEGORÍA', 'OBSERVACIÓN', 
               'PUNTO DE VENTA', 'CÓDIGO CENTRO COSTO', 'CENTRO COSTO PUNTO', 'FECHA SALIDA BODEGA']
    
    ws.append(headers)
    
    # Aplicar estilos a encabezados
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = header_alignment
        cell.border = border

    # Data
    for activo in activos:
        row = [
            activo.item,
            activo.documento or '',
            activo.nombres_apellidos or '',
            activo.imei1 or '',
            activo.imei2 or '',
            activo.sn or '',
            activo.mac_superflex or '',
            activo.marca or '',
            activo.activo or '',
            activo.cargo or '',
            activo.estado or '',
            activo.fecha_confirmacion.strftime('%d/%m/%Y') if activo.fecha_confirmacion else '',
            activo.responsable or '',
            activo.identificacion or '',
            activo.zona or '',
            str(activo.categoria) if activo.categoria else '',
            activo.observacion or '',
            activo.punto_venta or '',
            activo.codigo_centro_costo or '',
            activo.centro_costo_punto or '',
            activo.fecha_salida_bodega.strftime('%d/%m/%Y') if activo.fecha_salida_bodega else ''
        ]
        ws.append(row)
        
        # Aplicar bordes a las celdas de datos
        for cell in ws[ws.max_row]:
            cell.border = border

    # Ajustar ancho de columnas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width

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





# Trazabilidad CRUD
class TrazabilidadListView(LoginRequiredMixin, ListView):
    model = Trazabilidad
    template_name = 'activos/trazabilidad_list.html'
    context_object_name = 'movimientos'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para ver trazabilidad.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

# Trazabilidad registration
class RegistrarTrazabilidadView(LoginRequiredMixin, CreateView):
    model = Trazabilidad
    fields = ['tipo', 'zona_origen', 'zona_destino', 'estado_nuevo', 'descripcion']
    template_name = 'activos/registrar_trazabilidad.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['Admin', 'Logística']).exists():
            messages.error(request, 'No tienes permisos para registrar trazabilidad.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activo'] = get_object_or_404(Activo, pk=self.kwargs['pk'])
        # Obtener zonas únicas de los activos
        context['zonas'] = Activo.objects.values_list('zona', flat=True).distinct()
        return context

    def form_valid(self, form):
        activo = get_object_or_404(Activo, pk=self.kwargs['pk'])
        form.instance.activo = activo
        form.instance.usuario = self.request.user
        form.instance.estado_anterior = activo.estado

        if form.cleaned_data['estado_nuevo']:
            activo.estado = form.cleaned_data['estado_nuevo']
            activo.save()

        if form.cleaned_data['zona_destino']:
            activo.zona = form.cleaned_data['zona_destino']
            activo.save()

        messages.success(self.request, 'Trazabilidad registrada exitosamente.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('activos:activo_detail', kwargs={'pk': self.kwargs['pk']})


# Historial de activo
@login_required
def historial_activo(request, pk):
    activo = get_object_or_404(Activo, pk=pk)
    historial = Historial.objects.filter(activo=activo).order_by('-fecha')
    movimientos = Trazabilidad.objects.filter(activo=activo).order_by('-fecha')
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

    zona_nombre = request.GET.get('zona')
    if zona_nombre:
        activos = Activo.objects.filter(zona=zona_nombre)
    else:
        activos = Activo.objects.all()
        zona_nombre = None

    zonas = Activo.objects.values_list('zona', flat=True).distinct()
    return render(request, 'activos/reporte_por_zona.html', {
        'activos': activos,
        'zonas': zonas,
        'zona_seleccionada': zona_nombre,
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



# Zona CRUD

class ZonaListView(LoginRequiredMixin, ListView):
    model = Zona
    template_name = 'activos/zona_list.html'
    context_object_name = 'zonas'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaCreateView(LoginRequiredMixin, CreateView):
    model = Zona
    fields = '__all__'
    template_name = 'activos/zona_form.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaUpdateView(LoginRequiredMixin, UpdateView):
    model = Zona
    fields = '__all__'
    template_name = 'activos/zona_form.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class ZonaDeleteView(LoginRequiredMixin, DeleteView):
    model = Zona
    template_name = 'activos/zona_confirm_delete.html'
    success_url = reverse_lazy('activos:zona_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar zonas.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)


# Categoria CRUD

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'activos/category_list.html'
    context_object_name = 'categorias'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para ver categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    fields = '__all__'
    template_name = 'activos/category_form.html'
    success_url = reverse_lazy('activos:categoria_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para crear categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    fields = '__all__'
    template_name = 'activos/category_form.html'
    success_url = reverse_lazy('activos:categoria_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para editar categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'activos/category_confirm_delete.html'
    success_url = reverse_lazy('activos:categoria_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Admin').exists():
            messages.error(request, 'No tienes permisos para eliminar categorías.')
            return redirect('activos:home')
        return super().dispatch(request, *args, **kwargs)

