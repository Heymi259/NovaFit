from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.membresia import Plan, Membresia
from ..serializers.membresia_serializer import PlanSerializer, MembresiaSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Plan.objects.all()
        activo = self.request.query_params.get('activo')
        if activo is not None:
            queryset = queryset.filter(activo=activo.lower() == 'true')
        return queryset

    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        plan = self.get_object()
        plan.activo = True
        plan.save()
        return Response({'mensaje': f'Plan {plan.nombre} activado correctamente.'})

    @action(detail=True, methods=['post'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        plan = self.get_object()
        plan.activo = False
        plan.save()
        return Response({'mensaje': f'Plan {plan.nombre} desactivado correctamente.'})


class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.select_related('miembro__usuario', 'plan').all()
    serializer_class = MembresiaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Membresia.objects.select_related('miembro__usuario', 'plan').all()
        estado = self.request.query_params.get('estado')
        miembro_id = self.request.query_params.get('miembro')
        if estado:
            queryset = queryset.filter(estado=estado)
        if miembro_id:
            queryset = queryset.filter(miembro_id=miembro_id)
        return queryset

    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        membresia = self.get_object()
        membresia.estado = 'cancelada'
        membresia.save()
        return Response({'mensaje': 'Membresía cancelada correctamente.'})

    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        membresia = self.get_object()
        membresia.estado = 'activa'
        membresia.save()
        return Response({'mensaje': 'Membresía activada correctamente.'})
