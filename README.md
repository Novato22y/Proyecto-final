# 📚 Planeador Escolar - Proyecto Final

## 🎯 Descripción

Planeador Escolar es una aplicación web desarrollada con Flask que permite a los estudiantes organizar su vida académica. Ofrece gestión de horarios, materias, tareas, exámenes y notas. La versión actual incluye un panel de administración de usuarios y permite inicio de sesión con Google.

## 🏗️ Estructura del Proyecto

```
Proyecto-final/
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── models.py                # Modelo de datos (User)
│   ├── database.py              # Operaciones de base de datos
│   ├── routes.py                # Rutas y vistas principales
│   └── admin_routes.py          # Rutas para el panel de administración
├── static/                       # Archivos estáticos (CSS, JS, imágenes)
├── templates/                    # Plantillas HTML
│   ├── index.html               # Página principal
│   ├── sesion.html              # Página de inicio de sesión
│   ├── register.html            # Página de registro
│   ├── profile.html             # Página de perfil de usuario
│   ├── subject_detail.html      # Detalle de materia
│   └── admin_dashboard.html     # Panel de gestión de usuarios
├── config.py                    # Configuración de la aplicación
├── run.py                       # Punto de entrada principal
├── requirements.txt             # Dependencias del proyecto
└── README.md                    # Este archivo
```

## 🚀 Características

*   **Sistema de Autenticación:** Registro, inicio de sesión (Flask-Login) y página de perfil de usuario.
*   **Panel de Administración:** Vista protegida para administradores (`/admin/users`) que permite ver, eliminar y cambiar el rol de todos los usuarios.
*   **Gestión Académica:** Funcionalidad completa para crear, ver, editar y eliminar materias, tareas, exámenes y notas.


## 🛠️ Tecnologías

*   **Backend**: Python, Flask
*   **Base de Datos**: PostgreSQL
*   **Autenticación**: Flask-Login, Google OAuth 2.0
*   **Frontend**: HTML, CSS, JavaScript

## 🚀 Instalación y Ejecución

**1. Clonar y Preparar el Entorno**

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Proyecto-final

# Crear y activar un entorno virtual
python -m venv venv
# Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate

**2. Instalar dependencias**

Instala todas las dependencias necesarias para el proyecto ejecutando:
```bash
pip install -r requirements.txt
```
```
**2. Configurar la Aplicación y el archivo `.env`**
**2. Configurar la Aplicación**
El archivo `.env` es fundamental para el funcionamiento del login tradicional y el login con Google.
La aplicación utiliza variables de entorno para su configuración, lo que garantiza la seguridad de tus credenciales.
1.  **Crea tu archivo `.env`:**
1.  **Crea tu archivo `.env`:**
    Copia el archivo `.env.example` a un nuevo archivo llamado `.env` en la raíz de tu proyecto:
    ```bash
    cp .env.example .env
    ```
    (En Windows, puedes usar `copy .env.example .env`)
2.  **Edita el archivo `.env`:**
2.  **Edita el archivo `.env`:**
    Abre el archivo `.env` que acabas de crear y rellena las siguientes variables:

    *   **`SECRET_KEY`**: Una clave secreta única y segura para tu aplicación Flask.
    *   **Configuración de la Base de Datos:**
        *   `DB_HOST`: Host de tu base de datos PostgreSQL (ej. `localhost`).
        *   `DB_NAME`: Nombre de tu base de datos (ej. `planeador_escolar`).
        *   `DB_USER`: Usuario de tu base de datos.
        *   `DB_PASSWORD`: Contraseña de tu base de datos.
        *   `DB_PORT`: Puerto de tu base de datos (ej. `5432`).

    *   **Google Sign-In:** Si deseas usar el inicio de sesión con Google, obtén tus credenciales de la Consola de Desarrolladores de Google y añádelas aquí:
        **¿Dónde obtener las credenciales de Google?**
        - Ve a la [Consola de Desarrolladores de Google](https://console.developers.google.com/apis/credentials)
        - Crea un proyecto o selecciona uno existente.
        - Configura la pantalla de consentimiento OAuth.
        - Crea credenciales OAuth 2.0 tipo "Aplicación web".
        - Agrega los siguientes URLs en "URIs de redireccionamiento autorizados":
            - `http://127.0.0.1:5000/auth/google/callback`
            - `http://localhost:5000/auth/google/callback`
        - En "Orígenes autorizados de JavaScript":
            - `http://127.0.0.1:5000`
            - `http://localhost:5000`
        - Copia el `GOOGLE_CLIENT_ID` y el `GOOGLE_CLIENT_SECRET` y pégalos en tu `.env`.
        *   `GOOGLE_CLIENT_ID`: Tu ID de cliente de Google.
        *   `GOOGLE_CLIENT_SECRET`: Tu secreto de cliente de Google.

    Ejemplo de cómo debería verse tu archivo `.env`:
    ```
    SECRET_KEY='tu_clave_secreta_aqui'
    DB_HOST='localhost'
    DB_NAME='planeador_escolar'
    DB_USER='tu_usuario_db'
    DB_PASSWORD='tu_contraseña_db'
    DB_PORT='5432'
    GOOGLE_CLIENT_ID='tu-id-de-cliente-de-google.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET='tu-secreto-de-cliente-de-google'
**3. Funcionamiento actual y ejecución**
    El archivo `config.py` leerá automáticamente estos valores.
La aplicación se ejecutará en `http://127.0.0.1:5000`.
**3. Ejecutar la Aplicación**

```bash
python run.py
```
La aplicación se ejecutará en `http://127.0.0.1:5000`.

**Usuario Administrador por Defecto:**
- **Email**: `admin@planeador.com`
- **Contraseña**: `contraseña`
**Usuario Administrador por Defecto:**
*   **Email**: `admin@planeador.com`
*   **Contraseña**: `contraseña`

## 📈 Mejoras Futuras


- [ ] Sistema de notificaciones para tareas próximas
- [ ] Calendario visual mensual/anual
- [ ] Exportar horario a PDF/Excel
- [ ] Temas visuales personalizables

---


## 🛡️ Proceso de verificación de Google OAuth (para acceso con cualquier Gmail)





---
