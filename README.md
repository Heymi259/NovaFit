 🏋️ NovaFit API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST_Framework-3.17-ff1709?style=for-the-badge&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)
![Azure](https://img.shields.io/badge/Azure_VM-Deployed-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![CI/CD](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

**API REST para la gestión integral del gimnasio NovaFit**

[🌐 API en Producción](https://delacruz-gym.uaeftt-ute.site/api/) • [🔑 Admin](https://delacruz-gym.uaeftt-ute.site/admin/) • [📦 Repositorio](https://github.com/Heymi259/NovaFit)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Tecnologías](#tecnologías)
- [Diagrama de Base de Datos](#diagrama-de-base-de-datos)
- [Instalación y ejecución local](#instalación-y-ejecución-local)
- [Despliegue](#despliegue)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Colección Postman](#colección-postman)
- [Evaluación](#evaluación)

---

## 📖 Descripción

**NovaFit API** es una API REST completa para la gestión de un gimnasio. Permite administrar miembros, membresías, pagos, entrenadores, clases, inscripciones y asistencias con autenticación JWT y control de permisos por roles.

### Características principales

- ✅ CRUD completo para 9 entidades
- ✅ Autenticación JWT con roles (admin, entrenador, miembro)
- ✅ Filtros y paginación personalizada
- ✅ Despliegue en Azure VM con CI/CD automático
- ✅ Documentación completa con colección Postman

---

## 🛠 Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.12 | Lenguaje principal |
| Django | 6.0 | Framework web |
| Django REST Framework | 3.17 | API REST |
| PostgreSQL | 16 | Base de datos |
| djangorestframework-simplejwt | 5.5 | Autenticación JWT |
| django-filter | 25.2 | Filtros |
| Gunicorn | 26.0 | Servidor WSGI |
| Nginx | 1.24 | Proxy inverso |
| GitHub Actions | - | CI/CD |

---

## 🗄️ Diagrama de Base de Datos

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Usuario   │     │   Miembro   │     │ Entrenador  │
│─────────────│     │─────────────│     │─────────────│
│ id          │1───1│ id          │     │ id          │
│ username    │     │ usuario_id  │     │ usuario_id  │1
│ email       │     │ cedula      │     │ especialidad│
│ telefono    │1───1│ genero      │     │ biografia   │
│ rol         │     │ direccion   │     │ activo      │
│ password    │     │ foto        │     └──────┬──────┘
└─────────────┘     │ activo      │            │
                    └──────┬──────┘            │1
                           │1                  │
                           │         ┌─────────┴──────┐
                    ┌──────┴──────┐  │     Clase      │
                    │  Membresia  │  │────────────────│
                    │─────────────│  │ id             │
                    │ id          │  │ nombre         │
                    │ miembro_id  │  │ entrenador_id  │
                    │ plan_id     │  │ dia            │
                    │ fecha_inicio│  │ hora_inicio    │
                    │ fecha_fin   │  │ hora_fin       │
                    │ estado      │  │ capacidad      │
                    └──────┬──────┘  └───────┬────────┘
                           │1                │
                    ┌──────┴──────┐  ┌───────┴────────┐
                    │    Pago     │  │  Inscripcion   │
                    │─────────────│  │────────────────│
                    │ id          │  │ id             │
                    │ membresia_id│  │ miembro_id     │
                    │ monto       │  │ clase_id       │
                    │ metodo_pago │  │ estado         │
                    │ estado      │  └────────────────┘
                    └─────────────│
                                  │  ┌────────────────┐
                    ┌─────────────┐  │   Asistencia   │
                    │    Plan     │  │────────────────│
                    │─────────────│  │ id             │
                    │ id          │  │ miembro_id     │
                    │ nombre      │  │ clase_id       │
                    │ precio      │  │ hora_entrada   │
                    │ duracion    │  │ hora_salida    │
                    │ frecuencia  │  └────────────────┘
                    └─────────────┘
```

---

## ⚙️ Instalación y ejecución local

### Requisitos previos

- Python 3.12+
- PostgreSQL 16+
- uv (gestor de paquetes)

### 1. Clonar el repositorio

```bash
git clone https://github.com/Heymi259/NovaFit.git
cd NovaFit/novafit
```

### 2. Instalar dependencias

```bash
uv sync
```

### 3. Configurar variables de entorno

Crear un archivo `.env` en la carpeta `novafit/`:

```env
SECRET_KEY=novafit-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=novafitdb
DB_USER=novafituser
DB_PASSWORD=novafitpass
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOW_ALL_ORIGINS=True
TEST_DB_NAME=novafittestdb
```

### 4. Crear la base de datos PostgreSQL

```sql
CREATE USER novafituser WITH PASSWORD 'novafitpass';
CREATE DATABASE novafitdb OWNER novafituser;
```

### 5. Aplicar migraciones

```bash
uv run python manage.py migrate
```

### 6. Crear superusuario

```bash
uv run python manage.py createsuperuser
```

### 7. Ejecutar el servidor

```bash
uv run python manage.py runserver
```

✅ API disponible en: `http://localhost:8000/api/`
✅ Admin disponible en: `http://localhost:8000/admin/`

---

## 🚀 Despliegue

### URLs de producción

| Servicio | URL |
|----------|-----|
| 🌐 API | https://delacruz-gym.uaeftt-ute.site/api/ |
| 🔑 Admin | https://delacruz-gym.uaeftt-ute.site/admin/ |

### Infraestructura

```
GitHub → GitHub Actions → Azure VM (Ubuntu 24.04)
                              ├── Nginx (proxy reverso)
                              ├── Gunicorn (servidor WSGI)
                              ├── PostgreSQL (base de datos)
                              └── Let's Encrypt (SSL/TLS)
```

### CI/CD

El proyecto usa GitHub Actions para despliegue automático:

1. Se hace `push` a la rama `main`
2. GitHub Actions ejecuta los tests
3. Si los tests pasan ✅, despliega automáticamente en la VM

---

## 🔐 Autenticación

La API usa **JWT (JSON Web Tokens)** con tokens de acceso de 8 horas y refresh de 7 días.

### Obtener token

```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "tu_password"
}
```

**Respuesta:**

```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Usar el token en cada petición

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Roles y permisos

| Rol | Permisos |
|-----|----------|
| `admin` | Acceso total: crear, leer, actualizar, eliminar |
| `entrenador` | Gestionar clases y ver asistencias |
| `miembro` | Solo ver su propia información |

---

## 📡 Endpoints

### 🔑 Autenticación

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/login/` | Obtener token JWT | ❌ |
| POST | `/api/auth/refresh/` | Refrescar token | ❌ |
| POST | `/api/auth/verify/` | Verificar token | ❌ |

### 👤 Usuarios

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/usuarios/` | Listar usuarios | ✅ |
| POST | `/api/usuarios/` | Crear usuario | ✅ |
| GET | `/api/usuarios/{id}/` | Detalle | ✅ |
| PUT | `/api/usuarios/{id}/` | Actualizar | ✅ |
| DELETE | `/api/usuarios/{id}/` | Eliminar | ✅ |
| GET | `/api/usuarios/yo/` | Mi perfil | ✅ |
| PUT | `/api/usuarios/cambiar-password/` | Cambiar contraseña | ✅ |

### 🏃 Miembros

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/miembros/` | Listar miembros | ✅ |
| POST | `/api/miembros/` | Crear miembro | ✅ |
| GET | `/api/miembros/{id}/` | Detalle | ✅ |
| PUT | `/api/miembros/{id}/` | Actualizar | ✅ |
| DELETE | `/api/miembros/{id}/` | Eliminar | ✅ |
| POST | `/api/miembros/{id}/activar/` | Activar | ✅ |
| POST | `/api/miembros/{id}/desactivar/` | Desactivar | ✅ |

### 💳 Planes

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/planes/` | Listar planes | ✅ |
| POST | `/api/planes/` | Crear plan | ✅ |
| GET | `/api/planes/{id}/` | Detalle | ✅ |
| PUT | `/api/planes/{id}/` | Actualizar | ✅ |
| DELETE | `/api/planes/{id}/` | Eliminar | ✅ |
| POST | `/api/planes/{id}/activar/` | Activar | ✅ |
| POST | `/api/planes/{id}/desactivar/` | Desactivar | ✅ |

### 🎫 Membresías

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/membresias/` | Listar membresías | ✅ |
| POST | `/api/membresias/` | Crear membresía | ✅ |
| GET | `/api/membresias/{id}/` | Detalle | ✅ |
| PUT | `/api/membresias/{id}/` | Actualizar | ✅ |
| DELETE | `/api/membresias/{id}/` | Eliminar | ✅ |
| POST | `/api/membresias/{id}/activar/` | Activar | ✅ |
| POST | `/api/membresias/{id}/cancelar/` | Cancelar | ✅ |

### 💰 Pagos

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/pagos/` | Listar pagos | ✅ |
| POST | `/api/pagos/` | Registrar pago | ✅ |
| GET | `/api/pagos/{id}/` | Detalle | ✅ |
| PUT | `/api/pagos/{id}/` | Actualizar | ✅ |
| DELETE | `/api/pagos/{id}/` | Eliminar | ✅ |
| POST | `/api/pagos/{id}/completar/` | Completar | ✅ |
| POST | `/api/pagos/{id}/reembolsar/` | Reembolsar | ✅ |
| GET | `/api/pagos/resumen/` | Resumen total | ✅ |

### 🏋️ Entrenadores

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/entrenadores/` | Listar entrenadores | ✅ |
| POST | `/api/entrenadores/` | Crear entrenador | ✅ |
| GET | `/api/entrenadores/{id}/` | Detalle | ✅ |
| PUT | `/api/entrenadores/{id}/` | Actualizar | ✅ |
| DELETE | `/api/entrenadores/{id}/` | Eliminar | ✅ |
| GET | `/api/entrenadores/{id}/clases/` | Clases del entrenador | ✅ |

### 🧘 Clases

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/clases/` | Listar clases | ✅ |
| POST | `/api/clases/` | Crear clase | ✅ |
| GET | `/api/clases/{id}/` | Detalle | ✅ |
| PUT | `/api/clases/{id}/` | Actualizar | ✅ |
| DELETE | `/api/clases/{id}/` | Eliminar | ✅ |
| GET | `/api/clases/{id}/inscritos/` | Ver inscritos | ✅ |

### 📋 Inscripciones

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/inscripciones/` | Listar inscripciones | ✅ |
| POST | `/api/inscripciones/` | Crear inscripción | ✅ |
| GET | `/api/inscripciones/{id}/` | Detalle | ✅ |
| PUT | `/api/inscripciones/{id}/` | Actualizar | ✅ |
| DELETE | `/api/inscripciones/{id}/` | Eliminar | ✅ |
| POST | `/api/inscripciones/{id}/cancelar/` | Cancelar | ✅ |

### ✅ Asistencias

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| GET | `/api/asistencias/` | Listar asistencias | ✅ |
| POST | `/api/asistencias/` | Registrar asistencia | ✅ |
| GET | `/api/asistencias/{id}/` | Detalle | ✅ |
| PUT | `/api/asistencias/{id}/` | Actualizar | ✅ |
| DELETE | `/api/asistencias/{id}/` | Eliminar | ✅ |
| POST | `/api/asistencias/registrar-entrada/` | Registrar entrada | ✅ |
| POST | `/api/asistencias/{id}/registrar-salida/` | Registrar salida | ✅ |
| GET | `/api/asistencias/hoy/` | Asistencias de hoy | ✅ |

---

## 💡 Ejemplos de uso

### 1. Obtener token de acceso

```bash
curl -X POST https://delacruz-gym.uaeftt-ute.site/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Listar miembros activos

```bash
curl -X GET "https://delacruz-gym.uaeftt-ute.site/api/miembros/?activo=true" \
  -H "Authorization: Bearer <tu_token>"
```

### 3. Crear un plan de membresía

```bash
curl -X POST https://delacruz-gym.uaeftt-ute.site/api/planes/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Plan Premium",
    "precio": 60.00,
    "duracion_dias": 30,
    "frecuencia": "mensual",
    "max_clases_semana": 5
  }'
```

### 4. Registrar entrada de un miembro

```bash
curl -X POST https://delacruz-gym.uaeftt-ute.site/api/asistencias/registrar-entrada/ \
  -H "Authorization: Bearer <tu_token>" \
  -H "Content-Type: application/json" \
  -d '{"miembro_id": 1}'
```

### 5. Filtros disponibles

```bash
# Membresías activas de un miembro
GET /api/membresias/?estado=activa&miembro=1

# Clases del día lunes
GET /api/clases/?dia=lunes

# Pagos completados
GET /api/pagos/?estado=completado

# Paginación personalizada
GET /api/miembros/?page=1&page_size=5
```

---

## 📦 Colección Postman

Importar el archivo `novafit_postman.json` incluido en el repositorio en Postman o Thunder Client.

La colección incluye todos los endpoints con:
- Variables de entorno configuradas (`base_url`, `token`)
- Ejemplos de body para cada petición
- Headers de autenticación preconfigurados

---

## 📊 Evaluación del Proyecto

| Criterio | Peso | Implementación |
|----------|------|----------------|
| ✅ Funcionamiento del backend + conexión PostgreSQL | 30% | Django 6 + PostgreSQL 16 en Azure VM |
| ✅ CRUD y endpoints REST | 30% | 9 entidades con CRUD completo + acciones extra |
| ✅ Autenticación y permisos | 20% | JWT con roles admin/entrenador/miembro |
| ✅ Despliegue | 10% | Azure VM + Nginx + Gunicorn + SSL + CI/CD |
| ✅ Documentación | 10% | README completo + colección Postman |

---

## 📁 Estructura del proyecto

```
NovaFit/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD con GitHub Actions
└── novafit/
    ├── config/
    │   ├── settings.py         # Configuración principal
    │   ├── urls.py             # URLs del proyecto
    │   ├── wsgi.py
    │   └── asgi.py
    ├── novafit/
    │   ├── models/             # Modelos de BD
    │   │   ├── miembro.py
    │   │   ├── membresia.py
    │   │   ├── pago.py
    │   │   ├── entrenador.py
    │   │   ├── clase.py
    │   │   └── asistencia.py
    │   ├── serializers/        # Serializers DRF
    │   ├── views/              # Vistas y ViewSets
    │   ├── tests/              # Tests unitarios
    │   ├── migrations/         # Migraciones de BD
    │   ├── admin.py            # Panel de administración
    │   ├── apps.py
    │   ├── filters.py          # Filtros personalizados
    │   ├── pagination.py       # Paginación personalizada
    │   ├── permissions.py      # Permisos por rol
    │   └── urls.py             # URLs de la app
    ├── manage.py
    └── pyproject.toml          # Dependencias del proyecto
```

---

## 👤 Autor

<div align="center">

**Heymi De La Cruz**

Proyecto Final — NovaFit Gimnasio API

[![GitHub](https://img.shields.io/badge/GitHub-Heymi259-181717?style=for-the-badge&logo=github)](https://github.com/Heymi259/NovaFit)

</div>
