from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .vistas.miembro_views import UsuarioViewSet, MiembroViewSet
from .vistas.membresia_views import PlanViewSet, MembresiaViewSet
from .vistas.pago_views import PagoViewSet
from .vistas.entrenador_views import EntrenadorViewSet
from .vistas.clase_views import ClaseViewSet, InscripcionViewSet
from .vistas.asistencia_views import AsistenciaViewSet

router = DefaultRouter()

# Usuarios y Miembros
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'miembros', MiembroViewSet, basename='miembro')

# Membresías y Planes
router.register(r'planes', PlanViewSet, basename='plan')
router.register(r'membresias', MembresiaViewSet, basename='membresia')

# Pagos
router.register(r'pagos', PagoViewSet, basename='pago')

# Entrenadores
router.register(r'entrenadores', EntrenadorViewSet, basename='entrenador')

# Clases e Inscripciones
router.register(r'clases', ClaseViewSet, basename='clase')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')

# Asistencia
router.register(r'asistencias', AsistenciaViewSet, basename='asistencia')

urlpatterns = [
    path('', include(router.urls)),
]
