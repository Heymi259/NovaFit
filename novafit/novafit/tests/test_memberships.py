from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from ..models.miembro import Usuario, Miembro
from ..models.membresia import Plan, Membresia


class PlanTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin', password='admin1234', rol='admin'
        )
        self.plan = Plan.objects.create(
            nombre='Plan Básico',
            precio=30.00,
            duracion_dias=30,
            frecuencia='mensual'
        )
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_planes(self):
        url = reverse('plan-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_plan(self):
        url = reverse('plan-list')
        data = {
            'nombre': 'Plan Premium',
            'precio': 60.00,
            'duracion_dias': 30,
            'frecuencia': 'mensual'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_precio_invalido(self):
        url = reverse('plan-list')
        data = {
            'nombre': 'Plan Inválido',
            'precio': -10,
            'duracion_dias': 30,
            'frecuencia': 'mensual'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MembresiaTestCase(TestCase):
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
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_crear_membresia(self):
        url = reverse('membresia-list')
        data = {
            'miembro': self.miembro.id,
            'plan_id': self.plan.id,
            'fecha_inicio': date.today(),
            'fecha_fin': date.today() + timedelta(days=30),
            'estado': 'activa'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
