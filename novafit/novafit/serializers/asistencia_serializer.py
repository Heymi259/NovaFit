from rest_framework import serializers
from ..models.asistencia import Asistencia


class AsistenciaSerializer(serializers.ModelSerializer):
    nombre_miembro = serializers.SerializerMethodField()
    nombre_clase = serializers.SerializerMethodField()
    duracion_minutos = serializers.SerializerMethodField()

    class Meta:
        model = Asistencia
        fields = [
            'id', 'miembro', 'nombre_miembro',
            'clase', 'nombre_clase',
            'fecha_hora_entrada', 'fecha_hora_salida',
            'duracion_minutos', 'notas'
        ]
        read_only_fields = ['id', 'fecha_hora_entrada']

    def get_nombre_miembro(self, obj):
        return obj.miembro.usuario.get_full_name()

    def get_nombre_clase(self, obj):
        return obj.clase.nombre if obj.clase else 'Acceso libre'

    def get_duracion_minutos(self, obj):
        if obj.fecha_hora_entrada and obj.fecha_hora_salida:
            diferencia = obj.fecha_hora_salida - obj.fecha_hora_entrada
            return int(diferencia.total_seconds() / 60)
        return None

    def validate(self, data):
        if data.get('fecha_hora_salida') and data.get('fecha_hora_entrada'):
            if data['fecha_hora_salida'] <= data['fecha_hora_entrada']:
                raise serializers.ValidationError({'fecha_hora_salida': 'La hora de salida debe ser mayor a la de entrada.'})
        return data
