from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para el sistema de inventario.
    Extiende AbstractUser para mantener la funcionalidad base de Django.
    """
    
    ROLES = (
        ('admin', 'Admin'),
        ('logistica', 'Logística'),
        ('lectura', 'Lectura'),
        ('asignador', 'Asignador'),
    )
    
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default='lectura',
        verbose_name='Rol'
    )
    
    # Hacer el email opcional
    email = models.EmailField(
        verbose_name='Correo Electrónico',
        blank=True,
        null=False,
        default=''
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
    @property
    def is_admin(self):
        """Retorna True si el usuario es Admin"""
        return self.rol == 'admin'
    
    @property
    def is_logistica(self):
        """Retorna True si el usuario es Logística"""
        return self.rol == 'logistica'
    
    @property
    def is_lectura(self):
        """Retorna True si el usuario es Lectura"""
        return self.rol == 'lectura'
    
    @property
    def is_asignador(self):
        """Retorna True si el usuario es Asignador"""
        return self.rol == 'asignador'
