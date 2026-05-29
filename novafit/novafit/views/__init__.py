from .miembro_views import UsuarioViewSet, MiembroViewSet
from .membresia_views import PlanViewSet, MembresiaViewSet
from .pago_views import PagoViewSet
from .entrenador_views import EntrenadorViewSet
from .clase_views import ClaseViewSet, InscripcionViewSet
from .asistencia_views import AsistenciaViewSet

__all__ = [
    'UsuarioViewSet', 'MiembroViewSet',
    'PlanViewSet', 'MembresiaViewSet',
    'PagoViewSet',
    'EntrenadorViewSet',
    'ClaseViewSet', 'InscripcionViewSet',
    'AsistenciaViewSet',
]
