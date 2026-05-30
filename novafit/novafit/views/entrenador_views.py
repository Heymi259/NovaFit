from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.entrenador import Entrenador
from ..serializadores.entrenador_serializer import EntrenadorSerializer, EntrenadorResumenSerializer


class EntrenadorViewSet(viewsets.ModelViewSet):
    queryset = Entrenador.objects.select_related('usuario').all()
    serializer_class = EntrenadorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Entrenador.objects.select_related('usuario').all()
        activo = self.request.query_params.get('activo')
        especialidad = self.request.query_params.get('especialidad')
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        if especialidad:
            queryset = queryset.filter(especialidad__icontains=especialidad)
        return queryset

    @action(detail=True, methods=['get'], url_path='clases')
    def clases(self, request, pk=None):
        from ..serializadores.clase_serializer import ClaseSerializer
        entrenador = self.get_object()
        clases = entrenador.clases.filter(activa=True)
        serializer = ClaseSerializer(clases, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        entrenador = self.get_object()
        entrenador.activo = True
        entrenador.save()
        return Response({'mensaje': f'{entrenador} activado correctamente.'})

    @action(detail=True, methods=['post'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        entrenador = self.get_object()
        entrenador.activo = False
        entrenador.save()
        return Response({'mensaje': f'{entrenador} desactivado correctamente.'})
