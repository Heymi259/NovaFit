from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.miembro import Usuario, Miembro
from .models.membresia import Plan, Membresia
from .models.pago import Pago
from .models.entrenador import Entrenador
from .models.clase import Clase, Inscripcion
from .models.asistencia import Asistencia


# ── Usuario ──────────────────────────────────────────────────
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'is_active']
    list_filter = ['rol', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('NovaFit', {'fields': ('telefono', 'rol')}),
    )


# ── Miembro ───────────────────────────────────────────────────
@admin.register(Miembro)
class MiembroAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cedula', 'genero', 'activo', 'fecha_ingreso']
    list_filter = ['activo', 'genero']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'cedula']
    readonly_fields = ['fecha_ingreso', 'fecha_actualizacion']


# ── Plan ──────────────────────────────────────────────────────
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'duracion_dias', 'frecuencia', 'activo']
    list_filter = ['frecuencia', 'activo']
    search_fields = ['nombre']


# ── Membresia ─────────────────────────────────────────────────
@admin.register(Membresia)
class MembresiaAdmin(admin.ModelAdmin):
    list_display = ['miembro', 'plan', 'fecha_inicio', 'fecha_fin', 'estado']
    list_filter = ['estado', 'plan']
    search_fields = ['miembro__usuario__first_name', 'miembro__usuario__last_name']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']


# ── Pago ──────────────────────────────────────────────────────
@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['membresia', 'monto', 'metodo_pago', 'estado', 'fecha_pago']
    list_filter = ['estado', 'metodo_pago']
    search_fields = ['membresia__miembro__usuario__first_name']
    readonly_fields = ['fecha_pago', 'fecha_actualizacion']


# ── Entrenador ────────────────────────────────────────────────
@admin.register(Entrenador)
class EntrenadorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'especialidad', 'activo', 'fecha_ingreso']
    list_filter = ['activo']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'especialidad']
    readonly_fields = ['fecha_ingreso', 'fecha_actualizacion']


# ── Clase ─────────────────────────────────────────────────────
@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'entrenador', 'dia', 'hora_inicio', 'hora_fin', 'capacidad_maxima', 'activa']
    list_filter = ['dia', 'activa']
    search_fields = ['nombre', 'entrenador__usuario__first_name']


# ── Inscripcion ───────────────────────────────────────────────
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['miembro', 'clase', 'estado', 'fecha_inscripcion']
    list_filter = ['estado', 'clase']
    search_fields = ['miembro__usuario__first_name', 'clase__nombre']
    readonly_fields = ['fecha_inscripcion']


# ── Asistencia ────────────────────────────────────────────────
@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ['miembro', 'clase', 'fecha_hora_entrada', 'fecha_hora_salida']
    list_filter = ['clase']
    search_fields = ['miembro__usuario__first_name', 'miembro__usuario__last_name']
    readonly_fields = ['fecha_hora_entrada']
