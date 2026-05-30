from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    """Solo administradores pueden acceder."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'


class EsEntrenador(BasePermission):
    """Solo entrenadores pueden acceder."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'entrenador'


class EsMiembro(BasePermission):
    """Solo miembros pueden acceder."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'miembro'


class EsAdminOEntrenador(BasePermission):
    """Administradores o entrenadores pueden acceder."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol in ['admin', 'entrenador']


class EsAdminOLectura(BasePermission):
    """Admin puede todo, otros solo lectura."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.rol == 'admin'
