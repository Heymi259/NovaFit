from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views.miembro_views import UsuarioViewSet, MiembroViewSet
from .views.membresia_views import PlanViewSet, MembresiaViewSet
from .views.pago_views import PagoViewSet
from .views.entrenador_views import EntrenadorViewSet
from .views.clase_views import ClaseViewSet, InscripcionViewSet
from .views.asistencia_views import AsistenciaViewSet

router = DefaultRouter()

router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'miembros', MiembroViewSet, basename='miembro')
router.register(r'planes', PlanViewSet, basename='plan')
router.register(r'membresias', MembresiaViewSet, basename='membresia')
router.register(r'pagos', PagoViewSet, basename='pago')
router.register(r'entrenadores', EntrenadorViewSet, basename='entrenador')
router.register(r'clases', ClaseViewSet, basename='clase')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'asistencias', AsistenciaViewSet, basename='asistencia')

urlpatterns = [
    path('', include(router.urls)),
]