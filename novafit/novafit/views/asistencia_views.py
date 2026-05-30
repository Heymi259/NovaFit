from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from ..models.asistencia import Asistencia
from ..serializadores.asistencia_serializer import AsistenciaSerializer


class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.select_related('miembro__usuario', 'clase').all()
    serializer_class = AsistenciaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Asistencia.objects.select_related('miembro__usuario', 'clase').all()
        miembro_id = self.request.query_params.get('miembro')
        clase_id = self.request.query_params.get('clase')
        fecha = self.request.query_params.get('fecha')
        if miembro_id:
            queryset = queryset.filter(miembro_id=miembro_id)
        if clase_id:
            queryset = queryset.filter(clase_id=clase_id)
        if fecha:
            queryset = queryset.filter(fecha_hora_entrada__date=fecha)
        return queryset

    @action(detail=False, methods=['post'], url_path='registrar-entrada')
    def registrar_entrada(self, request):
        miembro_id = request.data.get('miembro_id')
        clase_id = request.data.get('clase_id')

        if not miembro_id:
            return Response(
                {'error': 'El miembro_id es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        asistencia = Asistencia.objects.create(
            miembro_id=miembro_id,
            clase_id=clase_id
        )
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='registrar-salida')
    def registrar_salida(self, request, pk=None):
        asistencia = self.get_object()
        if asistencia.fecha_hora_salida:
            return Response(
                {'error': 'Ya se registró la salida de este miembro.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        asistencia.fecha_hora_salida = timezone.now()
        asistencia.save()
        serializer = AsistenciaSerializer(asistencia)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='hoy')
    def hoy(self, request):
        hoy = timezone.now().date()
        asistencias = Asistencia.objects.filter(
            fecha_hora_entrada__date=hoy
        ).select_related('miembro__usuario', 'clase')
        serializer = AsistenciaSerializer(asistencias, many=True)
        return Response({
            'fecha': hoy,
            'total': asistencias.count(),
            'asistencias': serializer.data
        })
