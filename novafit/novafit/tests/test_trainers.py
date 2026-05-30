from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario
from ..models.entrenador import Entrenador


class EntrenadorTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin', password='admin1234', rol='admin'
        )
        self.usuario_entrenador = Usuario.objects.create_user(
            username='entrenador1', password='entrenador1234',
            first_name='Carlos', last_name='López', rol='entrenador'
        )
        self.entrenador = Entrenador.objects.create(
            usuario=self.usuario_entrenador,
            especialidad='Crossfit',
            biografia='Entrenador certificado con 5 años de experiencia.'
        )
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_entrenadores(self):
        url = reverse('entrenador-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalle_entrenador(self):
        url = reverse('entrenador-detail', args=[self.entrenador.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_desactivar_entrenador(self):
        url = reverse('entrenador-desactivar', args=[self.entrenador.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.entrenador.refresh_from_db()
        self.assertFalse(self.entrenador.activo)
