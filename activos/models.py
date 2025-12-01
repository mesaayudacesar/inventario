from django.db import models
from django.contrib.auth.models import User


class Zona(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Zona")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Zona"
        verbose_name_plural = "Zonas"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"





class Activo(models.Model):
    MARCA_CHOICES = [
        ('SUNMI V1', 'SUNMI V1'),
        ('SUNMI V2', 'SUNMI V2'),
        ('SUNMI V2 PRO', 'SUNMI V2 PRO'),
        ('N910', 'N910'),
        ('NEWLAND GRIS', 'NEWLAND GRIS'),
    ]

    item = models.AutoField(primary_key=True, verbose_name="ITEM")
    documento = models.CharField(max_length=100, blank=True, null=True, verbose_name="DOCUMENTO")
    nombres_apellidos = models.CharField(max_length=200, blank=True, null=True, verbose_name="NOMBRES Y APELLIDOS")
    imei1 = models.CharField(max_length=100, blank=True, null=True, verbose_name="IMEI 1")
    imei2 = models.CharField(max_length=100, blank=True, null=True, verbose_name="IMEI 2")
    sn = models.CharField(max_length=100, blank=True, null=True, verbose_name="S/N")
    mac_superflex = models.CharField(max_length=100, blank=True, null=True, verbose_name="MAC SUPERFLEX")
    marca = models.CharField(max_length=20, choices=MARCA_CHOICES, blank=True, null=True, verbose_name="MARCA")
    activo = models.CharField(max_length=100, blank=True, null=True, verbose_name="ACTIVO")
    cargo = models.CharField(max_length=100, default="vendedor ambulante", verbose_name="CARGO")
    estado = models.CharField(max_length=100, default="activo confirmado", verbose_name="ESTADO")
    fecha_confirmacion = models.DateField(auto_now_add=True, verbose_name="FECHA DE CONFIRMACIÓN")
    responsable = models.CharField(max_length=100, blank=True, null=True, verbose_name="RESPONSABLE")
    identificacion = models.CharField(max_length=100, blank=True, null=True, verbose_name="IDENTIFICACIÓN")
    zona = models.CharField(max_length=100, default="Valledupar", verbose_name="ZONA")
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoría")
    observacion = models.TextField(default="VERIFICADO", verbose_name="OBSERVACIÓN")
    punto_venta = models.CharField(max_length=100, blank=True, null=True, verbose_name="PUNTO DE VENTA")
    codigo_centro_costo = models.CharField(max_length=100, blank=True, null=True, verbose_name="CÓDIGO CENTRO DE COSTO")
    centro_costo_punto = models.CharField(max_length=100, blank=True, null=True, verbose_name="CENTRO DE COSTO PUNTO")
    fecha_salida_bodega = models.DateField(blank=True, null=True, verbose_name="FECHA DE SALIDA DE BODEGA")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Modificación")

    def __str__(self):
        return f"Activo {self.item} - {self.activo}"

    class Meta:
        verbose_name = "Activo"
        verbose_name_plural = "Activos"


class Trazabilidad(models.Model):
    TIPO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('salida', 'Salida'),
        ('transferencia', 'Transferencia'),
        ('cambio_estado', 'Cambio de Estado'),
    ]

    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, verbose_name="Activo")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Trazabilidad")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    zona_origen = models.CharField(max_length=100, blank=True, null=True, verbose_name="Zona Origen")
    zona_destino = models.CharField(max_length=100, blank=True, null=True, verbose_name="Zona Destino")
    estado_anterior = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado Anterior")
    estado_nuevo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Estado Nuevo")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"{self.tipo} - {self.activo} - {self.fecha}"

    class Meta:
        verbose_name = "Trazabilidad"
        verbose_name_plural = "Trazabilidad"
        ordering = ['-fecha']
        db_table = 'activos_trazabilidad'


class Historial(models.Model):
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, verbose_name="Activo")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    campo_cambiado = models.CharField(max_length=100, verbose_name="Campo Cambiado")
    valor_anterior = models.TextField(blank=True, null=True, verbose_name="Valor Anterior")
    valor_nuevo = models.TextField(blank=True, null=True, verbose_name="Valor Nuevo")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    def __str__(self):
        return f"Historial {self.activo} - {self.campo_cambiado}"

    class Meta:
        verbose_name = "Historial"
        verbose_name_plural = "Historiales"
