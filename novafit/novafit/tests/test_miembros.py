from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario, Miembro


class PruebaMiembros(TestCase):
    def setUp(self):
        self.cliente = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin',
            password='admin1234',
            rol='admin'
        )
        self.usuario_miembro = Usuario.objects.create_user(
            username='miembro1',
            password='miembro1234',
            first_name='Juan',
            last_name='Pérez',
            rol='miembro'
        )
        self.miembro = Miembro.objects.create(
            usuario=self.usuario_miembro,
            cedula='1234567890',
            genero='M'
        )
        url_login = reverse('token_obtain_pair')
        respuesta = self.cliente.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = respuesta.data['access']
        self.cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_miembros(self):
        url = reverse('miembro-list')
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)

    def test_detalle_miembro(self):
        url = reverse('miembro-detail', args=[self.miembro.id])
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)

    def test_activar_miembro(self):
        self.miembro.activo = False
        self.miembro.save()
        url = reverse('miembro-activar', args=[self.miembro.id])
        respuesta = self.cliente.post(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.miembro.refresh_from_db()
        self.assertTrue(self.miembro.activo)

    def test_desactivar_miembro(self):
        url = reverse('miembro-desactivar', args=[self.miembro.id])
        respuesta = self.cliente.post(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.miembro.refresh_from_db()
        self.assertFalse(self.miembro.activo)
