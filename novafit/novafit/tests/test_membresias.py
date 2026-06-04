from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta
from ..models.miembro import Usuario, Miembro
from ..models.membresia import Plan, Membresia


class PruebaPlanes(TestCase):
    def setUp(self):
        self.cliente = APIClient()
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
        respuesta = self.cliente.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = respuesta.data['access']
        self.cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_planes(self):
        url = reverse('plan-list')
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)

    def test_crear_plan(self):
        url = reverse('plan-list')
        datos = {
            'nombre': 'Plan Premium',
            'precio': 60.00,
            'duracion_dias': 30,
            'frecuencia': 'mensual'
        }
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)

    def test_precio_invalido(self):
        url = reverse('plan-list')
        datos = {
            'nombre': 'Plan Inválido',
            'precio': -10,
            'duracion_dias': 30,
            'frecuencia': 'mensual'
        }
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)


class PruebaMembresias(TestCase):
    def setUp(self):
        self.cliente = APIClient()
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
        respuesta = self.cliente.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = respuesta.data['access']
        self.cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_crear_membresia(self):
        url = reverse('membresia-list')
        datos = {
            'miembro': self.miembro.id,
            'plan_id': self.plan.id,
            'fecha_inicio': date.today(),
            'fecha_fin': date.today() + timedelta(days=30),
            'estado': 'activa'
        }
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
