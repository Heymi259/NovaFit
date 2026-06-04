from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario


class PruebaAutenticacion(TestCase):
    def setUp(self):
        self.cliente = APIClient()
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@novafit.com',
            password='test1234',
            first_name='Test',
            last_name='Usuario',
            rol='admin'
        )

    def test_login_exitoso(self):
        url = reverse('token_obtain_pair')
        datos = {'username': 'testuser', 'password': 'test1234'}
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertIn('access', respuesta.data)
        self.assertIn('refresh', respuesta.data)

    def test_login_fallido(self):
        url = reverse('token_obtain_pair')
        datos = {'username': 'testuser', 'password': 'contraseniaincorrecta'}
        respuesta = self.cliente.post(url, datos)
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acceso_sin_token(self):
        url = reverse('usuario-list')
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acceso_con_token(self):
        url_login = reverse('token_obtain_pair')
        datos = {'username': 'testuser', 'password': 'test1234'}
        respuesta = self.cliente.post(url_login, datos)
        token = respuesta.data['access']
        self.cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('usuario-list')
        respuesta = self.cliente.get(url)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
