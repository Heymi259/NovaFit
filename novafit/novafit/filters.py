import django_filters
from .models.miembro import Miembro
from .models.membresia import Plan, Membresia
from .models.pago import Pago
from .models.entrenador import Entrenador
from .models.clase import Clase
from .models.asistencia import Asistencia


class MiembroFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='usuario__first_name', lookup_expr='icontains')
    apellido = django_filters.CharFilter(field_name='usuario__last_name', lookup_expr='icontains')
    cedula = django_filters.CharFilter(lookup_expr='icontains')
    activo = django_filters.BooleanFilter()

    class Meta:
        model = Miembro
        fields = ['nombre', 'apellido', 'cedula', 'activo', 'genero']


class MembresiaFilter(django_filters.FilterSet):
    estado = django_filters.ChoiceFilter(choices=Membresia.ESTADOS)
    fecha_inicio = django_filters.DateFromToRangeFilter()
    fecha_fin = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Membresia
        fields = ['estado', 'plan', 'miembro']


class PagoFilter(django_filters.FilterSet):
    estado = django_filters.ChoiceFilter(choices=Pago.ESTADOS)
    metodo_pago = django_filters.ChoiceFilter(choices=Pago.METODOS)
    fecha_pago = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Pago
        fields = ['estado', 'metodo_pago']


class ClaseFilter(django_filters.FilterSet):
    dia = django_filters.ChoiceFilter(choices=Clase.DIAS)
    activa = django_filters.BooleanFilter()
    nombre = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Clase
        fields = ['dia', 'activa', 'entrenador']


class AsistenciaFilter(django_filters.FilterSet):
    fecha = django_filters.DateFilter(field_name='fecha_hora_entrada__date')
    fecha_rango = django_filters.DateFromToRangeFilter(field_name='fecha_hora_entrada__date')

    class Meta:
        model = Asistencia
        fields = ['miembro', 'clase']
