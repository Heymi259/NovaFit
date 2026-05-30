from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = [
        ('admin', 'Administrador'),
        ('entrenador', 'Entrenador'),
        ('miembro', 'Miembro'),
    ]

    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='miembro')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.get_full_name()} ({self.rol})'


class Miembro(models.Model):
    GENEROS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='miembro')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=GENEROS, blank=True)
    direccion = models.TextField(blank=True)
    cedula = models.CharField(max_length=20, unique=True, blank=True)
    foto = models.ImageField(upload_to='miembros/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f'{self.usuario.get_full_name()}'
