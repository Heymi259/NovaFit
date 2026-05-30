from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario, Miembro
from ..models.asistencia import Asistencia


class AsistenciaTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin', password='admin1234', rol='admin'
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

    def test_registrar_entrada(self):
        url = reverse('asistencia-registrar-entrada')
        data = {'miembro_id': self.miembro.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registrar_salida(self):
        asistencia = Asistencia.objects.create(miembro=self.miembro)
        url = reverse('asistencia-registrar-salida', args=[asistencia.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        asistencia.refresh_from_db()
        self.assertIsNotNone(asistencia.fecha_hora_salida)

    def test_asistencias_hoy(self):
        url = reverse('asistencia-hoy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
