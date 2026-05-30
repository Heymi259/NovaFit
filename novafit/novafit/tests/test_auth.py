from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@novafit.com',
            password='test1234',
            first_name='Test',
            last_name='User',
            rol='admin'
        )

    def test_login_exitoso(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'test1234'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fallido(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acceso_sin_token(self):
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_acceso_con_token(self):
        url_login = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'test1234'}
        response = self.client.post(url_login, data)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('usuario-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
