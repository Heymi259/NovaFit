from rest_framework.test import APIClient
from ..models.miembro import Usuario


def crear_usuario_y_token(username='testuser', password='test1234', rol='admin'):
    """Crea un usuario y retorna el cliente autenticado con su token."""
    from django.urls import reverse

    usuario = Usuario.objects.create_user(
        username=username,
        password=password,
        rol=rol
    )
    cliente = APIClient()
    respuesta = cliente.post(reverse('token_obtain_pair'), {
        'username': username,
        'password': password
    })
    token = respuesta.data['access']
    cliente.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return cliente, usuario


def obtener_token(cliente, username, password):
    """Obtiene el token JWT para un usuario existente."""
    from django.urls import reverse
    respuesta = cliente.post(reverse('token_obtain_pair'), {
        'username': username,
        'password': password
    })
    return respuesta.data.get('access')
