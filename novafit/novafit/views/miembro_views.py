from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.miembro import Usuario, Miembro
from ..serializadores.miembro_serializer import (
    UsuarioSerializer, RegistroUsuarioSerializer,
    MiembroSerializer, MiembroCrearSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistroUsuarioSerializer
        return UsuarioSerializer

    @action(detail=False, methods=['get'], url_path='yo')
    def yo(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='cambiar-password')
    def cambiar_password(self, request):
        usuario = request.user
        password_actual = request.data.get('password_actual')
        password_nueva = request.data.get('password_nueva')

        if not usuario.check_password(password_actual):
            return Response(
                {'error': 'La contraseña actual es incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        usuario.set_password(password_nueva)
        usuario.save()
        return Response({'mensaje': 'Contraseña actualizada correctamente.'})


class MiembroViewSet(viewsets.ModelViewSet):
    queryset = Miembro.objects.select_related('usuario').all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MiembroCrearSerializer
        return MiembroSerializer

    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        miembro = self.get_object()
        miembro.activo = True
        miembro.save()
        return Response({'mensaje': f'{miembro} activado correctamente.'})

    @action(detail=True, methods=['post'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        miembro = self.get_object()
        miembro.activo = False
        miembro.save()
        return Response({'mensaje': f'{miembro} desactivado correctamente.'})
