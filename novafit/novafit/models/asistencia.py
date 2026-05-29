from django.db import models


class Asistencia(models.Model):
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE, related_name='asistencias')
    clase = models.ForeignKey('Clase', on_delete=models.SET_NULL, null=True, blank=True, related_name='asistencias')
    fecha_hora_entrada = models.DateTimeField(auto_now_add=True)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'
        ordering = ['-fecha_hora_entrada']

    def __str__(self):
        return f'{self.miembro} - {self.fecha_hora_entrada.strftime("%d/%m/%Y %H:%M")}'
