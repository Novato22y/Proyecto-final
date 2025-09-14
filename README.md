git clone <url-del-repositorio>

# 📚 Planeador Escolar - Proyecto Final

## 🎯 Descripción

Planeador Escolar es una aplicación web desarrollada con Flask que permite a los estudiantes organizar su vida académica. Incluye gestión de horarios, materias, tareas, exámenes y notas, integración con Google Calendar y un panel de administración de usuarios.

## 🏗️ Estructura del Proyecto

```
Proyecto-final/
├── app/                          # Paquete principal de la aplicación
│   ├── __init__.py               # Factory de la aplicación Flask
│   ├── models.py                 # Modelos de datos
│   ├── database.py               # Operaciones de base de datos
│   ├── routes.py                 # Rutas y vistas principales
│   └── admin_routes.py           # Rutas para el panel de administración
├── static/                       # Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                    # Plantillas HTML
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── calendario.html
│   ├── principal.html
│   ├── profile.html
│   ├── prueba.html
│   ├── register.html
│   ├── sesion.html
│   └── subject_detail.html
├── config.py                     # Configuración de la aplicación
├── run.py                        # Punto de entrada principal
├── requirements.txt              # Dependencias del proyecto
├── .env                          # Variables de entorno (no se sube al repo)
├── .env.example                  # Ejemplo de configuración
├── politica_privacidad.html      # Página de política de privacidad
├── terminos_condiciones.html     # Página de términos y condiciones
├── TESTING.md                    # Guía de pruebas
└── README.md                     # Este archivo
```

## 🚀 Características

- **Sistema de Autenticación:** Registro, inicio de sesión (Flask-Login), inicio de sesión con Google y página de perfil de usuario.
- **Panel de Administración:** Vista protegida para administradores (`/admin/users`) para ver, eliminar y cambiar el rol de usuarios.
- **Gestión Académica:** Crear, ver, editar y eliminar materias, tareas, exámenes y notas.
- **Integración con Google Calendar:** Conexión y desconexión de cuenta, visualización de eventos.
- **Calendario interactivo:** Gestión de recordatorios por día, edición y eliminación desde el frontend.
- **Política de Privacidad y Términos:** Páginas informativas accesibles desde la app.

## 🛠️ Tecnologías

- **Backend:** Python, Flask
- **Base de Datos:** PostgreSQL
- **Autenticación:** Flask-Login, Google OAuth 2.0
- **Frontend:** HTML, CSS, JavaScript

## 🚀 Instalación y Ejecución

### 1. Clonar y Preparar el Entorno

```bash
git clone <url-del-repositorio>
cd Proyecto-final
python -m venv venv
# Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la Aplicación

El archivo `.env` es fundamental para el funcionamiento del login tradicional y el login con Google.

1. Copia el archivo `.env.example` a `.env`:
    ```bash
    cp .env.example .env
    ```
    (En Windows: `copy .env.example .env`)

2. Edita el archivo `.env` y rellena las variables:
    `SECRET_KEY`: Clave secreta para Flask.
    - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`: Configuración de PostgreSQL.
    - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Credenciales de Google OAuth.

    Ejemplo:
    ```
    SECRET_KEY='tu_clave_secreta_aqui'
    DB_HOST='localhost'
    DB_NAME='planeador_escolar'
    DB_USER='tu_usuario_db'
    DB_PASSWORD='tu_contraseña_db'
    DB_PORT='5432'
    GOOGLE_CLIENT_ID='tu-id-de-cliente-de-google.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET='tu-secreto-de-cliente-de-google'
    ```

### 4. Ejecutar la Aplicación

```bash
python run.py
```
La aplicación estará disponible en [http://127.0.0.1:5000](http://127.0.0.1:5000).

**Usuario Administrador por Defecto:**
- **Email**: `admin@planeador.com`
- **Contraseña**: `contraseña`

## 📈 Mejoras Futuras

- [ ] Sistema de notificaciones para tareas próximas
- [ ] Calendario visual mensual/anual
- [ ] Exportar horario a PDF/Excel
- [ ] Temas visuales personalizables

---

## 🛡️ Proceso de verificación de Google OAuth

Consulta la sección de configuración para conectar cualquier cuenta Gmail.

---

## 📖 Documentación de Pruebas

Consulta [TESTING.md](TESTING.md) para una guía detallada de pruebas de funcionalidades clave.

---

## 📦 Preparar para subir a GitHub

Antes de hacer push al repositorio remoto, este repositorio local fue limpiado de archivos de restauración (.bak) para evitar ruido en el historial. Los archivos fueron movidos a `backups/removed_baks/` dentro del proyecto por seguridad. Si necesitas restaurar algo, copia el archivo desde esa carpeta a su ubicación original.

Pasos recomendados para subir al remoto:

1. Asegúrate de tener un archivo `.gitignore` adecuado (ya incluido en el proyecto).
2. Añade los cambios:

```bash
git add .
git commit -m "Limpieza: eliminar archivos de respaldo y preparar repo para GitHub"
git remote add origin <url-del-repositorio>
git push -u origin main
```

Si quieres mantener una copia de seguridad fuera del repositorio antes del push, comprime `backups/removed_baks/` y guárdala en un almacenamiento seguro.

