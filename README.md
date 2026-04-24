# ⚽ Playrly Backend

> *Construyendo la infraestructura para que los equipos de barrio tengan su propia plataforma digital*

---

## 🎯 ¿Qué es esto?

**Playrly** es el backend de una plataforma para gestionar equipos, partidos y jugadores de fútbol amateur. Piensa en ello como el motor que permite:

- Registrar jugadores con toda su info (perfil completo)
- Crear equipos y asignar posiciones
- Organizar partidos entre equipos
- Registrar goles en tiempo real
- Sistema de confirmaciones para partidos

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    PLAYRLY BACKEND                      │
├─────────────────────────────────────────────────────────┤
│  Flask + SQLAlchemy + PostgreSQL                        │
│  ├── Auth (PyJWT + Werkzeug)                           │
│  ├── API RESTful                                       │
│  └── Migraciones con Alembic                           │
└─────────────────────────────────────────────────────────┘
```

### Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Framework** | Flask |
| **ORM** | SQLAlchemy |
| **DB** | PostgreSQL |
| **Migrations** | Flask-Migrate (Alembic) |
| **Auth** | PyJWT + Werkzeug |
| **Server** | Gunicorn + Eventlet |

---

## 📂 Estructura del Proyecto

```
backend/
├── playrly.py           # Entry point - crea la app Flask
├── models.py            # Todos los modelos SQLAlchemy
├── db.py                # Instancia de SQLAlchemy
├── wsgi.py              # Punto de entrada para Gunicorn
├── requirements.txt     # Dependencias
├── .env                 # Variables de entorno
├── migrations/          # Migraciones de Alembic
└── routes/              # Blueprints de la API
    ├── users.py         # CRUD de usuarios
    ├── teams.py         # Gestión de equipos
    ├── team_members.py  # Miembros de equipos
    ├── positions.py     # Posiciones (portero, defensa...)
    ├── system_roles.py  # Roles del sistema
    └── genders.py       # Catálogo de géneros
```

---

## 🚀 Quick Start

### 1. Setup inicial

```bash
# Clonar/entrar al proyecto
cd /mnt/d/Users/harld/Documents/playrly/backend

# Crear virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Crear archivo `.env`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/playrly
SECRET_KEY=tu-clave-secreta-super-segura
```

### 3. Base de datos

```bash
# Crear las tablas (usando migraciones)
flask db upgrade

# O si es primera vez
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. Correr el servidor

```bash
# Modo desarrollo
python playrly.py

# Modo producción
gunicorn -k eventlet -w 4 wsgi:app
```

---

## 📡 API Endpoints

### 👤 Usuarios (`/users`)

#### Crear usuario
```http
POST /users
Content-Type: application/json

{
  "nickname": "elcrack10",
  "email": "crack@example.com",
  "password": "supersecreto123",
  "names": "Juan",
  "surnames": "Pérez",
  "birthday": "1995-03-15",
  "id_gender": 1,
  "document_type_id": 1,
  "number_id": 123456789,
  "celphone": 3001234567,
  "address": "Calle 123 #45-67",
  "zipcode": "110111"
}
```

**Respuesta:**
```json
{
  "id_user": 1,
  "message": "Usuario creado correctamente"
}
```

> ⚠️ **Nota de seguridad:** Las contraseñas se hashean automáticamente con Werkzeug. Nunca se guardan en texto plano.

---

### ⚽ Equipos (`/teams`)

#### Crear equipo
```http
POST /teams
Content-Type: application/json

{
  "name": "Los cracks del barrio"
}
```

**Respuesta:**
```json
{
  "id_team": 1
}
```

---

### 👥 Miembros de Equipo (`/team_members`)

Unir un jugador a un equipo con posición específica:

```http
POST /team_members
Content-Type: application/json

{
  "id_user": 1,
  "id_team": 1,
  "id_position": 2,
  "jersey_number": 10,
  "is_admin": true
}
```

**Posiciones disponibles:**
- 1: Portero
- 2: Defensa
- 3: Mediocampista
- 4: Delantero

---

### 🎮 Partidos (`/matches`) - *Próximamente*

El modelo `Match` ya está definido. Endpoints en desarrollo:

```python
# Modelo actual (disponible en models.py)
class Match:
    - home_team_id: Equipo local
    - away_team_id: Equipo visitante
    - match_date: Fecha y hora
    - location: Lugar
    - status: SCHEDULED | IN_PROGRESS | FINISHED
    - created_by: Quién organizó el partido
```

#### Registrar gol

```http
POST /goals
Content-Type: application/json

{
  "match_id": 1,
  "team_id": 1,
  "player_id": 5,
  "minute": 23,
  "reported_by": 1
}
```

---

## 🗄️ Modelos de Datos

### Diagrama de Entidades

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│    USERS    │────<│ TEAM_MEMBERS │>────│    TEAMS    │
└─────────────┘     └──────────────┘     └─────────────┘
       │
       │            ┌─────────────┐
       └───────────<│    GOALS    │
                    └─────────────┘
                          │
                    ┌─────────────┐
                    │   MATCHES   │
                    └─────────────┘
```

### Entidades principales

| Entidad | Descripción |
|---------|-------------|
| **User** | Jugadores con perfil completo (datos personales, contacto) |
| **Team** | Equipos de fútbol |
| **TeamMember** | Relación usuario-equipo (con posición y número) |
| **Match** | Partidos programados entre dos equipos |
| **Goal** | Goles registrados (quién, cuándo, quién reportó) |
| **MatchConfirmation** | Confirmaciones de asistencia a partidos |
| **Position** | Catálogo: Portero, Defensa, Medio, Delantero |

---

## 🔐 Autenticación

El sistema usa **JWT** para autenticación. Flujo típico:

1. Usuario se registra (`POST /users`)
2. Usuario hace login (endpoint en desarrollo)
3. Recibe token JWT
4. Incluye token en header: `Authorization: Bearer <token>`

---

## 🛠️ Comandos Útiles

### Base de datos

```bash
# Crear nueva migración
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones
flask db upgrade

# Revertir última migración
flask db downgrade

# Ver historial
flask db history
```

### Servidor

```bash
# Desarrollo con hot-reload
FLASK_ENV=development flask run

# Producción con Gunicorn
gunicorn -k eventlet -w 4 --bind 0.0.0.0:5000 wsgi:app
```

---

## 📝 Roadmap

- [x] CRUD de usuarios con hashing de passwords
- [x] CRUD de equipos
- [x] Sistema de miembros y posiciones
- [ ] Endpoints de partidos (en progreso)
- [ ] Endpoints de goles
- [ ] Sistema de confirmaciones
- [ ] Autenticación JWT completa
- [ ] Validaciones de negocio
- [ ] Tests unitarios

---

## 🤝 Contribuir

1. Crear rama: `git checkout -b feature/nueva-funcionalidad`
2. Hacer cambios y commits
3. Push: `git push origin feature/nueva-funcionalidad`
4. Crear Pull Request

---

## 📄 Licencia

MIT - Haz lo que quieras, pero no me culpes si algo sale mal 😄

---

> *"El fútbol es simple, pero jugar simple es lo más difícil"* - Johan Cruyff
>
> Lo mismo aplica al código. 🎯

---

**Última actualización:** Abril 2025
**Versión:** 0.1.0-alpha
**Autor:** The Engineer
