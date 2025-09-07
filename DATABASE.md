# 📦 Estructura de la Base de Datos - Planeador Escolar

## Esquema principal: `users`

| Campo        | Tipo         | Descripción                                 |
|--------------|--------------|---------------------------------------------|
| id           | Integer      | Clave primaria, autoincremental             |
| email        | String(120)  | Correo electrónico, único, requerido        |
| password_hash| Text         | Hash de la contraseña (nullable para OAuth) |
| name         | String(100)  | Nombre completo del usuario                 |
| is_admin     | Boolean      | Si el usuario es administrador              |
| google_id    | String(120)  | ID de Google para login OAuth (opcional)    |

## Creación automática

- Al ejecutar `python run.py`, si la base de datos no existe, se crea automáticamente.
- Las tablas se crean usando SQLAlchemy (`db.create_all()`).

### ¿Cómo se crean las tablas automáticamente?

Cuando ejecutas el proyecto con `python run.py`, el sistema realiza lo siguiente:

- Verifica si la base de datos existe y la crea si es necesario (usando `psycopg2`).
- Inicializa la aplicación Flask y la extensión SQLAlchemy.
- Ejecuta el método `db.create_all()` dentro del contexto de la aplicación, lo que crea todas las tablas definidas en los modelos de Python (por ejemplo, la clase `User` en `app/models.py`).

No necesitas ejecutar comandos SQL manualmente para crear las tablas si usas el proyecto normalmente.

## Ejemplo de conexión

La URI de conexión se define en `config.py`:

```
postgresql://<usuario>:<contraseña>@<host>:<puerto>/<nombre_db>
```

## Migraciones

Para cambios futuros, considera usar [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) para gestionar migraciones de esquema.

---

**Nota:** Si usas otro modelo, agrega aquí su estructura.


## Comandos útiles para borrar la base de datos y las tablas

## Comandos SQL para crear la base de datos y la tabla users manualmente

### Crear la base de datos (PostgreSQL)

Ejecuta esto en tu cliente SQL:

```sql
CREATE DATABASE planeador_escolar;
```

### Crear la tabla users

Ejecuta esto en tu cliente SQL (dentro de la base de datos):

```sql
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(120) UNIQUE NOT NULL,
	password_hash TEXT,
	name VARCHAR(100) NOT NULL,
	is_admin BOOLEAN NOT NULL DEFAULT FALSE,
	google_id VARCHAR(120) UNIQUE
);
```

### Borrar solo las tablas (mantener la base de datos)

Ejecuta estas sentencias SQL en tu cliente de base de datos:

```sql
DROP TABLE IF EXISTS users CASCADE;
```

### Borrar la base de datos completa (PostgreSQL)

Ejecuta esta sentencia SQL en tu cliente de base de datos (debes estar fuera de la base de datos que quieres borrar):

```sql
DROP DATABASE IF EXISTS <nombre_db>;
```

Ejemplo:

```sql
DROP DATABASE IF EXISTS planeador_escolar;
```
