from rest_framework import serializers
from ..modelos.miembro import Usuario, Miembro


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'rol']
        read_only_fields = ['id']


class RegistroUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirmar_password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'telefono', 'rol', 'password', 'confirmar_password']

    def validate(self, data):
        if data['password'] != data['confirmar_password']:
            raise serializers.ValidationError({'confirmar_password': 'Las contraseñas no coinciden.'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirmar_password')
        password = validated_data.pop('password')
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario


class MiembroSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = Miembro
        fields = [
            'id', 'usuario', 'nombre_completo', 'fecha_nacimiento',
            'genero', 'direccion', 'cedula', 'foto',
            'activo', 'fecha_ingreso', 'fecha_actualizacion'
        ]
        read_only_fields = ['id', 'fecha_ingreso', 'fecha_actualizacion']

    def get_nombre_completo(self, obj):
        return obj.usuario.get_full_name()


class MiembroCrearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Miembro
        fields = ['fecha_nacimiento', 'genero', 'direccion', 'cedula', 'foto']
