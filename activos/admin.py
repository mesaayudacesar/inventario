from django.contrib import admin
from .models import Activo, Historial

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('item', 'activo', 'marca', 'estado', 'responsable', 'fecha_confirmacion')
    list_filter = ('marca', 'estado', 'zona', 'fecha_confirmacion')
    search_fields = ('item', 'activo', 'imei1', 'imei2', 'sn', 'documento', 'nombres_apellidos')
    ordering = ('item',)
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')

    def has_add_permission(self, request):
        return request.user.groups.filter(name__in=['Administrador', 'Bodega']).exists()

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        # Lógica de permisos basada en roles
        if request.user.groups.filter(name='Administrador').exists():
            return True
        elif request.user.groups.filter(name='Bodega').exists():
            # Bodega puede editar ciertos campos
            return True
        elif request.user.groups.filter(name='Asignador').exists():
            # Asignador puede editar campos de asignación
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Administrador').exists()

    def save_model(self, request, obj, form, change):
        if change:
            # Registrar cambios en historial
            for field in form.changed_data:
                Historial.objects.create(
                    activo=obj,
                    usuario=request.user,
                    campo_cambiado=field,
                    valor_anterior=form.initial.get(field),
                    valor_nuevo=getattr(obj, field)
                )
        super().save_model(request, obj, form, change)

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('activo', 'usuario', 'campo_cambiado', 'fecha')
    list_filter = ('campo_cambiado', 'fecha')
    search_fields = ('activo__item', 'usuario__username', 'campo_cambiado')
    readonly_fields = ('activo', 'usuario', 'campo_cambiado', 'valor_anterior', 'valor_nuevo', 'fecha')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Administrador').exists()
