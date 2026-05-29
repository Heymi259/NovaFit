from rest_framework import serializers
from ..modelos.membresia import Plan, Membresia


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = [
            'id', 'nombre', 'descripcion', 'precio',
            'duracion_dias', 'frecuencia', 'max_clases_semana',
            'activo', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError('El precio debe ser mayor a 0.')
        return value

    def validate_duracion_dias(self, value):
        if value <= 0:
            raise serializers.ValidationError('La duración debe ser mayor a 0 días.')
        return value


class MembresiaSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(), source='plan', write_only=True
    )
    nombre_miembro = serializers.SerializerMethodField()

    class Meta:
        model = Membresia
        fields = [
            'id', 'miembro', 'nombre_miembro', 'plan', 'plan_id',
            'fecha_inicio', 'fecha_fin', 'estado',
            'notas', 'fecha_creacion', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_creacion', 'fecha_actualizacion']

    def get_nombre_miembro(self, obj):
        return obj.miembro.usuario.get_full_name()

    def validate(self, data):
        if data['fecha_inicio'] >= data['fecha_fin']:
            raise serializers.ValidationError({'fecha_fin': 'La fecha fin debe ser mayor a la fecha inicio.'})
        return data
