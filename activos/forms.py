from django import forms
from .models import Activo, Zona, Categoria, Marca
from django.utils import timezone


class ActivoForm(forms.ModelForm):
    ESTADO_CHOICES_CREATE = [
        ('activo confirmado', 'Activo Confirmado'),
        ('asignado', 'Asignado'),
    ]
    
    ESTADO_CHOICES_UPDATE = [
        ('activo confirmado', 'Activo Confirmado'),
        ('asignado', 'Asignado'),
        ('dado de baja', 'Dado de Baja'),
    ]
    
    CARGO_CHOICES = [
        ('vendedor ambulante', 'Vendedor Ambulante'),
        ('vendedor', 'Vendedor'),
        ('administrativos', 'Administrativos'),
    ]
    
    class Meta:
        model = Activo
        exclude = ['fecha_confirmacion', 'fecha_creacion', 'fecha_modificacion', 'marca_old']
        widgets = {
            'documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el documento',
                'list': 'documento-list'
            }),
            'nombres_apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombres y apellidos',
                'list': 'nombres-list'
            }),
            'categoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'marca': forms.Select(attrs={'class': 'form-select', 'id': 'id_marca'}),
            'zona': forms.Select(attrs={'class': 'form-select'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del responsable'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Identificación del responsable',
                'list': 'identificacion-list'
            }),
            'codigo_centro_costo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del centro de costo',
                'list': 'codigo-centro-list'
            }),
            'centro_costo_punto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del centro de costo',
                'list': 'nombre-centro-list'
            }),
            'observacion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese observaciones',
                'rows': 1,
                'style': 'overflow:hidden; resize:none;'
            }),
            'imei1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IMEI 1'}),
            'imei2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'IMEI 2'}),
            'sn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie'}),
            'iccid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ICCID', 'id': 'id_iccid'}),
            'operador': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'id': 'id_operador'}),
            'mac_superflex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MAC Superflex'}),
            'activo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del activo'}),
            'punto_venta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Punto de venta'}),
            'fecha_salida_bodega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        is_update = kwargs.pop('is_update', False)
        super().__init__(*args, **kwargs)
        
        # Configurar choices para estado según si es creación o edición
        if is_update:
            self.fields['estado'].widget.choices = self.ESTADO_CHOICES_UPDATE
        else:
            self.fields['estado'].widget.choices = self.ESTADO_CHOICES_CREATE
            self.fields['estado'].initial = 'activo confirmado'
        
        # Configurar choices para cargo
        self.fields['cargo'].widget = forms.Select(attrs={'class': 'form-select'})
        self.fields['cargo'].widget.choices = self.CARGO_CHOICES
        self.fields['cargo'].initial = 'vendedor ambulante'
        
        # Configurar zona como select con las zonas existentes
        zonas = Zona.objects.all().values_list('nombre', 'nombre')
        self.fields['zona'].widget = forms.Select(attrs={'class': 'form-select'})
        self.fields['zona'].widget.choices = [('', '')] + list(zonas)
        
        # Configurar categoría para que no muestre "----"
        self.fields['categoria'].empty_label = None
        
        # Configurar marca: si hay una categoría seleccionada, filtrar marcas
        if self.instance.pk and self.instance.categoria:
            # Si estamos editando y hay una categoría, filtrar marcas
            self.fields['marca'].queryset = Marca.objects.filter(categoria=self.instance.categoria)
        else:
            # Si estamos creando, mostrar todas las marcas (el filtrado se hará con JavaScript)
            self.fields['marca'].queryset = Marca.objects.all()
        
        # Configurar marca para que no muestre "----" si hay opciones
        if self.fields['marca'].queryset.exists():
            self.fields['marca'].empty_label = "Seleccione una marca"
        
        # Hacer obligatorios todos los campos de la sección "Datos del Activo"
        campos_obligatorios = [
            'categoria', 'marca', 'activo', 'sn', 
            'imei1', 'imei2', 'estado', 'zona', 
            'responsable', 'identificacion'
        ]
        
        for campo in campos_obligatorios:
            if campo in self.fields:
                self.fields[campo].required = True
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Establecer fecha_confirmacion si es un nuevo activo
        if not instance.pk:
            instance.fecha_confirmacion = timezone.now().date()
        
        # Actualizar estado basado en documento y nombres
        if instance.documento and instance.nombres_apellidos:
            if instance.estado == 'activo confirmado':
                instance.estado = 'asignado'
        
        if commit:
            instance.save()
        return instance
