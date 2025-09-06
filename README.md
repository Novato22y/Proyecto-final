# 📚 Planeador Escolar - Proyecto Final

## 🎯 Descripción

Planeador Escolar es una aplicación web desarrollada con Flask que permite a los estudiantes organizar su vida académica. Ofrece gestión de horarios, materias, tareas, exámenes y notas. La versión actual incluye un panel de administración de usuarios y se integra con Google Calendar.

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
*   **Integración con Google Calendar:** Conexión opcional a la cuenta de Google del usuario para visualizar sus próximos eventos en la página principal.

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
    *   **Google Calendar (Opcional):** Si deseas usar la integración con Google Calendar, obtén tus credenciales de la Consola de Desarrolladores de Google y añádelas aquí:
        **¿Dónde obtener las credenciales de Google?**
        - Ve a la [Consola de Desarrolladores de Google](https://console.developers.google.com/apis/credentials)
        - Crea un proyecto o selecciona uno existente.
        - Configura la pantalla de consentimiento OAuth.
        - Crea credenciales OAuth 2.0 tipo "Aplicación web".
        - Agrega los siguientes URLs en "URIs de redireccionamiento autorizados":
            - `http://127.0.0.1:5000/auth/google/callback`
            - `http://localhost:5000/auth/google/callback`
            - (y si usas Google Calendar) `http://127.0.0.1:5000/callback` y `http://localhost:5000/callback`
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

- [x] Integración con Google Calendar
- [ ] Sistema de notificaciones para tareas próximas
- [ ] Calendario visual mensual/anual
- [ ] Exportar horario a PDF/Excel
- [ ] Temas visuales personalizables

---


## 🛡️ Proceso de verificación de Google OAuth (para acceso con cualquier Gmail)

Si quieres que cualquier usuario pueda iniciar sesión con Google y vincular Google Calendar (no solo los testers), debes completar el proceso de verificación de Google OAuth. Google lo exige cuando solicitas permisos sensibles como acceso a Calendar.

### Pasos para la verificación:

1. Ve a la [Pantalla de consentimiento OAuth](https://console.cloud.google.com/apis/credentials/consent) en Google Cloud.
2. Completa todos los campos obligatorios:
    - Nombre de la app
    - Logo de la app (JPG, PNG, BMP, cuadrado, 120x120 px)
    - Correo de contacto del desarrollador
    - Página principal de la aplicación (puedes usar tu repositorio de GitHub o una página informativa)
    - [Política de privacidad](https://www.freeprivacypolicy.com/) (puedes generar una gratuita)
    - [Condiciones de servicio](https://www.freeprivacypolicy.com/free-terms-and-conditions-generator/) (puedes generar una gratuita)
3. Agrega los dominios autorizados si tienes una web pública.
4. Inicia el proceso de verificación en la sección “Centro de verificación” o “Verification”.
5. Google revisará tu app y, si todo está correcto, la aprobará para cualquier usuario.

**Enlaces útiles:**

**Ejemplo de enlaces para la verificación:**
- Política de privacidad: [https://novato22y.github.io/Proyecto-final/politica_privacidad.html](https://novato22y.github.io/Proyecto-final/politica_privacidad.html)
- Términos y condiciones: [https://novato22y.github.io/Proyecto-final/terminos_condiciones.html](https://novato22y.github.io/Proyecto-final/terminos_condiciones.html)

Puedes crear estos archivos en tu repositorio y publicarlos con GitHub Pages, o incluirlos en la carpeta raíz del proyecto como `politica_privacidad.html` y `terminos_condiciones.html`.
Si usas GitHub Pages, los enlaces serán accesibles públicamente y válidos para la verificación de Google.

**Importante:**

---
## 🛠️ Actualización: Integración de Google Sign-In y Refactorización a SQLAlchemy (En Progreso)

Se está llevando a cabo una actualización importante para modernizar el backend y añadir la funcionalidad de "Inicio de Sesión con Google".

### ✅ Cambios Realizados

1.  **Dependencias (`requirements.txt`)**: Añadida la librería `Authlib` para OAuth 2.0.
2.  **Configuración (`config.py`)**: Añadida la `GOOGLE_DISCOVERY_URL` para `Authlib`.
3.  **Modelo de Datos (`app/models.py`)**: Refactorizada la clase `User` para que sea un modelo de SQLAlchemy, añadiendo el campo `google_id` y métodos de gestión de contraseñas.
4.  **Fábrica de la App (`app/__init__.py`)**: Actualizada para inicializar SQLAlchemy y Authlib, y para que el `user_loader` de Flask-Login use el nuevo modelo.
5.  **Rutas (`app/routes.py`)**: Añadidas las rutas para el flujo de Google Sign-In y refactorizadas las rutas de login/registro estándar para usar SQLAlchemy.

### ⏳ Tareas Pendientes

Para finalizar la implementación, quedan los siguientes pasos:

*   **Backend:**
    - [ ] **Limpiar `app/database.py`**: Eliminar las funciones de creación y gestión de usuarios (`create_tables` para users, `user_exists`, `create_user`, `create_admin_user`) que han quedado obsoletas.
    - [ ] **Centralizar la Creación de la BD**: Modificar `run.py` para que se encargue de crear todas las tablas al iniciar la aplicación.
    - [ ] **Limpiar `app/routes.py`**: Eliminar la llamada a `init_db()`.

*   **Frontend y Puesta en Marcha:**
    - [ ] **Añadir Botón de Google**: Insertar el código HTML del botón en `sesion.html` y `register.html`.
    - [ ] **Instalar Dependencias**: Ejecutar `pip install -r requirements.txt`.
    - [ ] **Reiniciar la Base de Datos**: Eliminar las tablas antiguas para que la aplicación cree las nuevas con la estructura correcta.