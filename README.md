git clone <url-del-repositorio>

# 📚 Planeador Escolar - Proyecto Final

## 🎯 Descripción

Planeador Escolar es una aplicación web desarrollada con Flask que permite a los estudiantes organizar su vida académica. Actualmente, la versión principal incluye:

- Sistema de autenticación (registro, login tradicional y con Google)
- Panel de administración de usuarios
- Estructura modular y lista para escalar nuevas funcionalidades

> **Nota:** Las funcionalidades de materias, tareas, exámenes, notas y horarios han sido eliminadas para una futura reconstrucción desde cero.

---

## 🏗️ Estructura del Proyecto (2025)

```
Proyecto-final/
├── app/
│   ├── __init__.py              # Factory de la aplicación Flask
│   ├── models.py                # Modelo de datos (User)
│   ├── database.py              # Conexión a la base de datos
│   ├── routes.py                # Rutas principales (login, registro, perfil)
│   └── admin_routes.py          # Rutas para el panel de administración
├── static/
│   ├── css/                     # Estilos CSS
│   ├── images/                  # Imágenes
│   ├── js/
│   │   ├── core/                # Módulos JS reutilizables (ej. reloj)
│   │   ├── main.js              # Punto de entrada JS principal (ES Modules)
│   │   └── ...                  # Futuras carpetas para nuevas funcionalidades
├── templates/
│   ├── index.html               # Página principal
│   ├── sesion.html              # Login
│   ├── register.html            # Registro
│   ├── profile.html             # Perfil de usuario
│   ├── admin_dashboard.html     # Panel de administración de usuarios
│   └── subject_detail.html      # (Plantilla limpia para futuras materias)
├── config.py                    # Configuración Flask
├── run.py                       # Punto de entrada principal
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
```

---

## 🚀 Instalación y Ejecución

1. **Clona el repositorio y prepara el entorno**

    ```bash
    git clone <url-del-repositorio>
    cd Proyecto-final
    python -m venv venv
    # Windows: venv\Scripts\activate | Linux/Mac: source venv/bin/activate
    ```

2. **Instala las dependencias**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configura el archivo `.env`**

    Copia `.env.example` a `.env` y completa las variables:

    - `SECRET_KEY`: Clave secreta Flask
    - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`: Datos de conexión PostgreSQL
    - `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`: Credenciales de Google OAuth

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

4. **Ejecuta la aplicación**

    ```bash
    python run.py
    ```
    Accede en [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 👤 Usuario Administrador por Defecto

- **Email:** `admin@planeador.com`
- **Contraseña:** `contraseña`

---

## 🛠️ Tecnologías

- **Backend:** Python, Flask
- **Base de Datos:** PostgreSQL
- **Autenticación:** Flask-Login, Google OAuth 2.0
- **Frontend:** HTML, CSS, JavaScript (ES Modules)

---

## 🧩 Estructura JavaScript Modular

- Todos los scripts JS están organizados por módulos en `static/js/`.
- El punto de entrada es `main.js`, que importa módulos como el reloj desde `core/clock.js`.
- Puedes agregar nuevas carpetas para futuras funcionalidades y usar `import/export`.

---

## 🛡️ Mantenimiento y Escalabilidad

- Documenta y comenta tu código.
- Elimina archivos y dependencias no usados.
- Usa Blueprints y módulos para nuevas funcionalidades.
- Implementa pruebas automáticas.
- Mantén actualizado el archivo `requirements.txt`.
- Considera migraciones con Flask-Migrate para cambios en la base de datos.
- Revisa y actualiza dependencias de seguridad.

---

## 📈 Mejoras Futuras

- [ ] Sistema de notificaciones
- [ ] Calendario visual
- [ ] Exportar datos a PDF/Excel
- [ ] Temas visuales personalizables
- [ ] Reconstrucción de gestión académica (materias, tareas, exámenes, notas)

---

## � Contacto y Contribución

¿Quieres contribuir? Abre un issue o un pull request. ¡Toda ayuda es bienvenida!
---
