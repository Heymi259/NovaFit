from rest_framework import serializers
from ..models.clase import Clase, Inscripcion
from .entrenador_serializer import EntrenadorResumenSerializer


class ClaseSerializer(serializers.ModelSerializer):
    entrenador = EntrenadorResumenSerializer(read_only=True)
    entrenador_id = serializers.PrimaryKeyRelatedField(
        queryset=Clase.objects.none(), source='entrenador', write_only=True, allow_null=True
    )
    total_inscritos = serializers.SerializerMethodField()

    class Meta:
        model = Clase
        fields = [
            'id', 'nombre', 'descripcion', 'entrenador', 'entrenador_id',
            'dia', 'hora_inicio', 'hora_fin', 'capacidad_maxima',
            'total_inscritos', 'activa', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']

    def get_total_inscritos(self, obj):
        return obj.inscripciones.filter(estado='activa').count()

    def validate(self, data):
        if data.get('hora_inicio') and data.get('hora_fin'):
            if data['hora_inicio'] >= data['hora_fin']:
                raise serializers.ValidationError({'hora_fin': 'La hora fin debe ser mayor a la hora inicio.'})
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..models.entrenador import Entrenador
        self.fields['entrenador_id'].queryset = Entrenador.objects.filter(activo=True)


class InscripcionSerializer(serializers.ModelSerializer):
    nombre_miembro = serializers.SerializerMethodField()
    nombre_clase = serializers.SerializerMethodField()

    class Meta:
        model = Inscripcion
        fields = [
            'id', 'miembro', 'nombre_miembro',
            'clase', 'nombre_clase',
            'estado', 'fecha_inscripcion'
        ]
        read_only_fields = ['id', 'fecha_inscripcion']

    def get_nombre_miembro(self, obj):
        return obj.miembro.usuario.get_full_name()

    def get_nombre_clase(self, obj):
        return obj.clase.nombre

    def validate(self, data):
        clase = data.get('clase')
        if clase:
            inscritos_activos = clase.inscripciones.filter(estado='activa').count()
            if inscritos_activos >= clase.capacidad_maxima:
                raise serializers.ValidationError({'clase': 'La clase ya alcanzó su capacidad máxima.'})
        return data
