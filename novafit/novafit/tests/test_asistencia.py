from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario, Miembro
from ..models.asistencia import Asistencia


class PruebaAsistencias(TestCase):
    def setUp(self):
        self.cliente = APIClient()
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
        respuesta = self.cliente.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = respuesta.data['access']
        self.cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_registrar_entrada(self):
        url = reverse('asistencia-registrar-entrada')
        datos = {'miembro_id': self.miembro.id}
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)

    def test_registrar_salida(self):
        asistencia = Asistencia.objects.create(miembro=self.miembro)
        url = reverse('asistencia-registrar-salida', args=[asistencia.id])
        respuesta = self.cliente.post(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        asistencia.refresh_from_db()
        self.assertIsNotNone(asistencia.fecha_hora_salida)

    def test_asistencias_hoy(self):
        url = reverse('asistencia-hoy')
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
