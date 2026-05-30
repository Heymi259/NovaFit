from django.db import models


class Entrenador(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE, related_name='entrenador')
    especialidad = models.CharField(max_length=200)
    certificaciones = models.TextField(blank=True)
    biografia = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'

    def __str__(self):
        return f'{self.usuario.get_full_name()} - {self.especialidad}'
