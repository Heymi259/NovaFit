from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()])),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('last_name', models.CharField(blank=True, max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('entrenador', 'Entrenador'), ('miembro', 'Miembro')], default='miembro', max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.permission')),
            ],
            options={'verbose_name': 'Usuario', 'verbose_name_plural': 'Usuarios'},
            managers=[('objects', django.contrib.auth.models.UserManager())],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('genero', models.CharField(blank=True, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('direccion', models.TextField(blank=True)),
                ('cedula', models.CharField(blank=True, max_length=20, unique=True)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='miembros/')),
                ('activo', models.BooleanField(default=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='miembro', to='novafit.usuario')),
            ],
            options={'verbose_name': 'Miembro', 'verbose_name_plural': 'Miembros', 'ordering': ['-fecha_ingreso']},
        ),
        migrations.CreateModel(
            name='Entrenador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('especialidad', models.CharField(max_length=200)),
                ('certificaciones', models.TextField(blank=True)),
                ('biografia', models.TextField(blank=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='entrenador', to='novafit.usuario')),
            ],
            options={'verbose_name': 'Entrenador', 'verbose_name_plural': 'Entrenadores'},
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('duracion_dias', models.PositiveIntegerField()),
                ('frecuencia', models.CharField(choices=[('mensual', 'Mensual'), ('trimestral', 'Trimestral'), ('semestral', 'Semestral'), ('anual', 'Anual')], default='mensual', max_length=20)),
                ('max_clases_semana', models.PositiveIntegerField(blank=True, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Plan', 'verbose_name_plural': 'Planes', 'ordering': ['precio']},
        ),
        migrations.CreateModel(
            name='Membresia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField()),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('vencida', 'Vencida'), ('cancelada', 'Cancelada'), ('pendiente', 'Pendiente')], default='pendiente', max_length=20)),
                ('notas', models.TextField(blank=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='membresias', to='novafit.miembro')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='membresias', to='novafit.plan')),
            ],
            options={'verbose_name': 'Membresía', 'verbose_name_plural': 'Membresías', 'ordering': ['-fecha_inicio']},
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=8)),
                ('metodo_pago', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia'), ('otro', 'Otro')], default='efectivo', max_length=20)),
                ('estado', models.CharField(choices=[('completado', 'Completado'), ('pendiente', 'Pendiente'), ('fallido', 'Fallido'), ('reembolsado', 'Reembolsado')], default='pendiente', max_length=20)),
                ('referencia', models.CharField(blank=True, max_length=100)),
                ('comprobante', models.FileField(blank=True, null=True, upload_to='comprobantes/')),
                ('notas', models.TextField(blank=True)),
                ('fecha_pago', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('membresia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagos', to='novafit.membresia')),
            ],
            options={'verbose_name': 'Pago', 'verbose_name_plural': 'Pagos', 'ordering': ['-fecha_pago']},
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('dia', models.CharField(choices=[('lunes', 'Lunes'), ('martes', 'Martes'), ('miercoles', 'Miércoles'), ('jueves', 'Jueves'), ('viernes', 'Viernes'), ('sabado', 'Sábado'), ('domingo', 'Domingo')], max_length=10)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('capacidad_maxima', models.PositiveIntegerField(default=20)),
                ('activa', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('entrenador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clases', to='novafit.entrenador')),
            ],
            options={'verbose_name': 'Clase', 'verbose_name_plural': 'Clases', 'ordering': ['dia', 'hora_inicio']},
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('cancelada', 'Cancelada')], default='activa', max_length=20)),
                ('fecha_inscripcion', models.DateTimeField(auto_now_add=True)),
                ('clase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='novafit.clase')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscripciones', to='novafit.miembro')),
            ],
            options={'verbose_name': 'Inscripción', 'verbose_name_plural': 'Inscripciones', 'unique_together': {('miembro', 'clase')}},
        ),
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_entrada', models.DateTimeField(auto_now_add=True)),
                ('fecha_hora_salida', models.DateTimeField(blank=True, null=True)),
                ('notas', models.TextField(blank=True)),
                ('clase', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asistencias', to='novafit.clase')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asistencias', to='novafit.miembro')),
            ],
            options={'verbose_name': 'Asistencia', 'verbose_name_plural': 'Asistencias', 'ordering': ['-fecha_hora_entrada']},
        ),
    ]