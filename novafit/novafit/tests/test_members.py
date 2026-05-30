from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario, Miembro


class MiembroTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin',
            password='admin1234',
            rol='admin'
        )
        self.miembro_usuario = Usuario.objects.create_user(
            username='miembro1',
            password='miembro1234',
            first_name='Juan',
            last_name='Pérez',
            rol='miembro'
        )
        self.miembro = Miembro.objects.create(
            usuario=self.miembro_usuario,
            cedula='1234567890',
            genero='M'
        )
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_miembros(self):
        url = reverse('miembro-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalle_miembro(self):
        url = reverse('miembro-detail', args=[self.miembro.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activar_miembro(self):
        self.miembro.activo = False
        self.miembro.save()
        url = reverse('miembro-activar', args=[self.miembro.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.miembro.refresh_from_db()
        self.assertTrue(self.miembro.activo)

    def test_desactivar_miembro(self):
        url = reverse('miembro-desactivar', args=[self.miembro.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.miembro.refresh_from_db()
        self.assertFalse(self.miembro.activo)
