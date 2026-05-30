from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models.miembro import Usuario, Miembro
from ..models.entrenador import Entrenador
from ..models.clase import Clase, Inscripcion


class ClaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = Usuario.objects.create_user(
            username='admin', password='admin1234', rol='admin'
        )
        self.usuario_entrenador = Usuario.objects.create_user(
            username='entrenador1', password='entrenador1234', rol='entrenador'
        )
        self.entrenador = Entrenador.objects.create(
            usuario=self.usuario_entrenador, especialidad='Yoga'
        )
        self.clase = Clase.objects.create(
            nombre='Yoga Matutino',
            entrenador=self.entrenador,
            dia='lunes',
            hora_inicio='07:00',
            hora_fin='08:00',
            capacidad_maxima=15
        )
        url_login = reverse('token_obtain_pair')
        response = self.client.post(url_login, {'username': 'admin', 'password': 'admin1234'})
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_listar_clases(self):
        url = reverse('clase-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_clase(self):
        url = reverse('clase-list')
        data = {
            'nombre': 'Pilates',
            'entrenador_id': self.entrenador.id,
            'dia': 'martes',
            'hora_inicio': '09:00',
            'hora_fin': '10:00',
            'capacidad_maxima': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_inscritos_clase(self):
        url = reverse('clase-inscritos', args=[self.clase.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
