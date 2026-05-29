from rest_framework import serializers
from ..modelos.pago import Pago


class PagoSerializer(serializers.ModelSerializer):
    nombre_miembro = serializers.SerializerMethodField()
    nombre_plan = serializers.SerializerMethodField()

    class Meta:
        model = Pago
        fields = [
            'id', 'membresia', 'nombre_miembro', 'nombre_plan',
            'monto', 'metodo_pago', 'estado',
            'referencia', 'comprobante', 'notas',
            'fecha_pago', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_pago', 'fecha_actualizacion']

    def get_nombre_miembro(self, obj):
        return obj.membresia.miembro.usuario.get_full_name()

    def get_nombre_plan(self, obj):
        return obj.membresia.plan.nombre

    def validate_monto(self, value):
        if value <= 0:
            raise serializers.ValidationError('El monto debe ser mayor a 0.')
        return value


class PagoResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'monto', 'metodo_pago', 'estado', 'fecha_pago']
        read_only_fields = ['id', 'fecha_pago']
