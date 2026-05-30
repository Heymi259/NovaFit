from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from ..models.miembro import Usuario, Miembro
from ..models.membresia import Plan, Membresia
from ..models.pago import Pago


class PagoTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin', password='admin1234', rol='admin'
        )
        self.plan = Plan.objects.create(
            nombre='Plan Básico', precio=30.00,
            duracion_dias=30, frecuencia='mensual'
        )
        self.usuario_miembro = Usuario.objects.create_user(
            username='miembro1', password='miembro1234', rol='miembro'
        )
        self.miembro = Miembro.objects.create(
            usuario=self.usuario_miembro, cedula='1234567890'
        )
        self.membresia = Membresia.objects.create(
            miembro=self.miembro, plan=self.plan,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30),
            estado='activa'
        )
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_crear_pago(self):
        url = reverse('pago-list')
        data = {
            'membresia': self.membresia.id,
            'monto': 30.00,
            'metodo_pago': 'efectivo',
            'estado': 'pendiente'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_completar_pago(self):
        pago = Pago.objects.create(
            membresia=self.membresia, monto=30.00,
            metodo_pago='efectivo', estado='pendiente'
        )
        url = reverse('pago-completar', args=[pago.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        pago.refresh_from_db()
        self.assertEqual(pago.estado, 'completado')

    def test_monto_invalido(self):
        url = reverse('pago-list')
        data = {
            'membresia': self.membresia.id,
            'monto': -5,
            'metodo_pago': 'efectivo'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
