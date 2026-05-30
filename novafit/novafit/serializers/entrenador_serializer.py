from rest_framework import serializers
from ..models.entrenador import Entrenador
from .miembro_serializer import UsuarioSerializer


class EntrenadorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Entrenador
        fields = [
            'id', 'usuario', 'nombre_completo', 'especialidad',
            'certificaciones', 'biografia',
            'activo', 'fecha_ingreso', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_ingreso', 'fecha_actualizacion']

    def get_nombre_completo(self, obj):
        return obj.usuario.get_full_name()


class EntrenadorResumenSerializer(serializers.ModelSerializer):
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Entrenador
        fields = ['id', 'nombre_completo', 'especialidad']

    def get_nombre_completo(self, obj):
        return obj.usuario.get_full_name()
