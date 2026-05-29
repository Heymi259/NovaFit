from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..modelos.pago import Pago
from ..serializadores.pago_serializer import PagoSerializer, PagoResumenSerializer


class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.select_related('membresia__miembro__usuario', 'membresia__plan').all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Pago.objects.select_related(
            'membresia__miembro__usuario', 'membresia__plan'
        ).all()
        estado = self.request.query_params.get('estado')
        metodo = self.request.query_params.get('metodo_pago')
        miembro_id = self.request.query_params.get('miembro')
        if estado:
            queryset = queryset.filter(estado=estado)
        if metodo:
            queryset = queryset.filter(metodo_pago=metodo)
        if miembro_id:
            queryset = queryset.filter(membresia__miembro_id=miembro_id)
        return queryset

    @action(detail=True, methods=['post'], url_path='completar')
    def completar(self, request, pk=None):
        pago = self.get_object()
        pago.estado = 'completado'
        pago.save()
        return Response({'mensaje': 'Pago marcado como completado.'})

    @action(detail=True, methods=['post'], url_path='reembolsar')
    def reembolsar(self, request, pk=None):
        pago = self.get_object()
        if pago.estado != 'completado':
            return Response(
                {'error': 'Solo se pueden reembolsar pagos completados.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        pago.estado = 'reembolsado'
        pago.save()
        return Response({'mensaje': 'Pago reembolsado correctamente.'})

    @action(detail=False, methods=['get'], url_path='resumen')
    def resumen(self, request):
        from django.db.models import Sum, Count
        total = Pago.objects.filter(estado='completado').aggregate(
            total=Sum('monto'), cantidad=Count('id')
        )
        return Response({
            'total_recaudado': total['total'] or 0,
            'cantidad_pagos': total['cantidad'] or 0,
        })
