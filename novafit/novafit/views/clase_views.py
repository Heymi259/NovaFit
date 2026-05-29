from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..modelos.clase import Clase, Inscripcion
from ..serializadores.clase_serializer import ClaseSerializer, InscripcionSerializer


class ClaseViewSet(viewsets.ModelViewSet):
    queryset = Clase.objects.select_related('entrenador__usuario').all()
    serializer_class = ClaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Clase.objects.select_related('entrenador__usuario').all()
        dia = self.request.query_params.get('dia')
        activa = self.request.query_params.get('activa')
        entrenador_id = self.request.query_params.get('entrenador')
        if dia:
            queryset = queryset.filter(dia=dia)
        if activa is not None:
            queryset = queryset.filter(activa=activa.lower() == 'true')
        if entrenador_id:
            queryset = queryset.filter(entrenador_id=entrenador_id)
        return queryset

    @action(detail=True, methods=['get'], url_path='inscritos')
    def inscritos(self, request, pk=None):
        from ..serializadores.miembro_serializer import MiembroSerializer
        clase = self.get_object()
        inscritos = clase.inscripciones.filter(estado='activa').select_related('miembro__usuario')
        miembros = [i.miembro for i in inscritos]
        serializer = MiembroSerializer(miembros, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        clase = self.get_object()
        clase.activa = True
        clase.save()
        return Response({'mensaje': f'Clase {clase.nombre} activada correctamente.'})

    @action(detail=True, methods=['post'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        clase = self.get_object()
        clase.activa = False
        clase.save()
        return Response({'mensaje': f'Clase {clase.nombre} desactivada correctamente.'})


class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.select_related('miembro__usuario', 'clase').all()
    serializer_class = InscripcionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Inscripcion.objects.select_related('miembro__usuario', 'clase').all()
        miembro_id = self.request.query_params.get('miembro')
        clase_id = self.request.query_params.get('clase')
        estado = self.request.query_params.get('estado')
        if miembro_id:
            queryset = queryset.filter(miembro_id=miembro_id)
        if clase_id:
            queryset = queryset.filter(clase_id=clase_id)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        inscripcion = self.get_object()
        inscripcion.estado = 'cancelada'
        inscripcion.save()
        return Response({'mensaje': 'Inscripción cancelada correctamente.'})
