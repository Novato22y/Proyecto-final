# 📚 EduNote - Planeador Escolar

## 🎯 Descripción

**EduNote** es una aplicación web moderna desarrollada con Flask que permite a estudiantes y educadores organizar eficientemente su vida académica. La aplicación ofrece un sistema completo de gestión de tareas, recordatorios, calendario interactivo, autenticación segura con múltiples opciones y un panel administrativo robusto.

## ✨ Características Principales

### 🔐 Sistema de Autenticación Avanzado
- **Registro y Login Tradicional**: Sistema seguro con hash de contraseñas
- **Google OAuth 2.0**: Inicio de sesión con cuenta de Google
- **Gestión de Sesiones**: Manejo seguro de sesiones con Flask-Login
- **Perfil de Usuario**: Subida de foto de perfil, cambio de nombre y contraseña

### 📅 Sistema de Calendario y Recordatorios
- **API REST Completa**: Endpoints para crear, leer, actualizar y eliminar recordatorios
- **Calendario Interactivo**: Visualización por fechas con funcionalidad dinámica
- **Niveles de Importancia**: Clasificación de recordatorios (alta, media, baja)
- **Gestión por Usuario**: Recordatorios asociados a cada usuario autenticado

### 🛡️ Panel de Administración
- **Gestión de Usuarios**: Ver lista completa de usuarios registrados
- **Control de Roles**: Promoción/degradación de usuarios administradores
- **Eliminación Segura**: Eliminación de usuarios con validaciones
- **Protección de Rutas**: Middleware de seguridad para acceso administrativo

### 🎨 Interfaz de Usuario Moderna
- **Diseño Responsivo**: Adaptable a diferentes dispositivos
- **Sidebar Dinámico**: Navegación intuitiva con iconografía SVG
- **Reloj en Tiempo Real**: Widget de fecha y hora actualizado dinámicamente
- **Tema Nocturno**: Iconografía que sugiere modo nocturno/diurno

## 🏗️ Arquitectura del Proyecto

```
proyecto_final/
├── app/                          # Paquete principal de la aplicación Flask
│   ├── __init__.py              # Factory Pattern - Configuración de la app
│   ├── models.py                # Modelos SQLAlchemy (User, Recordatorio)
│   ├── database.py              # Funciones de conexión PostgreSQL
│   ├── routes.py                # Rutas principales y API endpoints
│   └── admin_routes.py          # Rutas del panel administrativo
├── static/                       # Recursos estáticos del frontend
│   ├── css/
│   │   ├── styles.css           # Estilos principales (896 líneas)
│   │   ├── principal.css        # Estilos específicos página principal
│   │   ├── register.css         # Estilos formulario registro
│   │   ├── sesion.css           # Estilos formulario login
│   │   └── emergencia.css       # Estilos de emergencia/fallback
│   ├── js/
│   │   ├── principal.js         # Lógica reloj y funciones principales
│   │   ├── calendario.js        # Funcionalidad del calendario
│   │   ├── main.js              # Funciones generales
│   │   ├── script.js            # Scripts adicionales
│   │   ├── sidebar-social.js    # Funcionalidad sidebar social
│   │   └── core/
│   │       └── clock.js         # Funciones específicas del reloj
│   └── images/
│       ├── logoedunote.*        # Logos en múltiples formatos
│       ├── user_default.png     # Avatar por defecto
│       └── profiles/            # Fotos de perfil de usuarios
├── templates/                    # Plantillas Jinja2
│   ├── base.html               # Template base con sidebar
│   ├── principal.html          # Dashboard principal
│   ├── profile.html            # Perfil de usuario
│   ├── register.html           # Formulario de registro
│   ├── sesion.html             # Formulario de login
│   ├── calendario.html         # Vista del calendario
│   ├── admin_dashboard.html    # Panel de administración
│   ├── subject_detail.html     # Detalle de materias
│   └── prueba.html             # Template de pruebas
├── config.py                    # Configuración centralizada
├── run.py                       # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno (no incluido)
├── politica_privacidad.html     # Página de políticas
├── terminos_condiciones.html    # Términos y condiciones
└── TESTING.md                   # Documentación de pruebas
```

## 🛠️ Stack Tecnológico

### Backend
- **Flask 3.1.1**: Framework web principal
- **SQLAlchemy**: ORM para manejo de base de datos
- **PostgreSQL**: Base de datos relacional principal
- **Flask-Login**: Gestión de autenticación y sesiones
- **Authlib**: Implementación OAuth 2.0 para Google Sign-In
- **Werkzeug**: Utilidades de seguridad y hash de contraseñas

### Frontend
- **HTML5/CSS3**: Estructura y estilos
- **JavaScript ES6**: Funcionalidad del lado cliente
- **Google Fonts (Inter)**: Tipografía moderna
- **SVG Icons**: Iconografía vectorial escalable

### Infraestructura
- **psycopg2**: Adaptador PostgreSQL para Python
- **python-dotenv**: Gestión de variables de entorno
- **setuptools/pip**: Gestión de dependencias

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8+ instalado
- PostgreSQL 12+ instalado y configurado
- Git instalado
- Cuenta de Google Cloud (para OAuth)

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Novato22y/Proyecto-final.git
cd Proyecto-final
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos PostgreSQL
```sql
-- Conectarse a PostgreSQL y crear la base de datos
CREATE DATABASE planeador_escolar;
CREATE USER tu_usuario WITH PASSWORD 'tu_contraseña';
GRANT ALL PRIVILEGES ON DATABASE planeador_escolar TO tu_usuario;
```

### 5. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# Configuración Flask
SECRET_KEY=tu_clave_secreta_muy_larga_y_aleatoria_aqui
DEBUG=True

# Configuración PostgreSQL
DB_HOST=localhost
DB_NAME=planeador_escolar
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_PORT=5432

# Configuración Google OAuth (opcional)
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret
```

### 6. Configurar Google OAuth (Opcional)
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar Google+ API
4. Crear credenciales OAuth 2.0
5. Agregar `http://127.0.0.1:5000/google/callback` como URI de redirección
6. Copiar Client ID y Client Secret al archivo `.env`

### 7. Inicializar la Aplicación
```bash
python run.py
```

La aplicación estará disponible en: `http://127.0.0.1:5000`

### 8. Credenciales de Administrador
**Usuario administrador creado automáticamente:**
- **Email**: admin@planeador.com
- **Contraseña**: contraseña

## 📋 API Endpoints

### Autenticación
- `GET /register` - Mostrar formulario de registro
- `POST /register` - Procesar registro de usuario
- `GET /login` - Mostrar formulario de login
- `POST /login` - Procesar login
- `GET /logout` - Cerrar sesión
- `GET /google/login` - Iniciar OAuth con Google
- `GET /google/callback` - Callback OAuth Google

### Recordatorios API
- `GET /api/recordatorios/<fecha>` - Obtener recordatorios por fecha
- `POST /api/recordatorios` - Crear nuevo recordatorio
- `PUT /api/recordatorios/<id>` - Actualizar recordatorio
- `DELETE /api/recordatorios/<id>` - Eliminar recordatorio

### Perfil de Usuario
- `GET /profile` - Ver perfil del usuario
- `POST /upload_profile_photo` - Subir foto de perfil
- `POST /update_password` - Cambiar contraseña
- `POST /update_name` - Cambiar nombre

### Panel de Administración
- `GET /admin/users` - Listar todos los usuarios
- `POST /admin/delete_user/<id>` - Eliminar usuario
- `POST /admin/update_role/<id>` - Cambiar rol de usuario

## 🔧 Funcionalidades Detalladas

### Sistema de Recordatorios
```javascript
// Ejemplo de uso de la API de recordatorios
const nuevoRecordatorio = {
    fecha: '2024-12-25',
    titulo: 'Examen Final',
    descripcion: 'Estudiar capítulos 1-10',
    importancia: 'alta'
};

fetch('/api/recordatorios', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(nuevoRecordatorio)
});
```

### Autenticación Dual
La aplicación soporta tanto autenticación tradicional como OAuth:
- **Tradicional**: Hash seguro de contraseñas con Werkzeug
- **Google OAuth**: Integración completa con Authlib
- **Sesiones**: Gestión automática con Flask-Login

### Panel Administrativo
Funcionalidades exclusivas para administradores:
- Vista de todos los usuarios registrados
- Cambio de roles (admin/usuario)
- Eliminación de usuarios con validaciones
- Protección mediante decorador `@login_required`

## 🔒 Seguridad Implementada

### Autenticación y Autorización
- Hash de contraseñas con `werkzeug.security`
- Validación de sesiones con Flask-Login
- Protección CSRF implícita en formularios
- Middleware de autorización para rutas admin

### Validaciones de Entrada
- Sanitización de datos de formularios
- Validación de tipos de archivo para uploads
- Verificación de longitud de contraseñas
- Validación de formato de email

### Configuración Segura
- Variables sensibles en archivo `.env`
- Separación de configuración por entornos
- Conexión segura a base de datos
- Tokens OAuth manejados server-side

## 🧪 Testing y Calidad

### Estructura de Pruebas
Consulta `TESTING.md` para:
- Casos de prueba detallados
- Escenarios de usuario
- Validación de endpoints
- Pruebas de seguridad

### Estándares de Código
- Documentación inline en español
- Separación clara de responsabilidades
- Factory Pattern para configuración
- Blueprint Pattern para organización de rutas

## 🚀 Deployment

### Preparación para Producción
```bash
# Instalar dependencias de producción
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Variables de Entorno Producción
```env
SECRET_KEY=clave_super_secreta_produccion
DEBUG=False
DB_HOST=tu_servidor_postgres
# ... resto de configuración
```

## 🤝 Contribución

### Estructura de Commits
- `feat:` Nuevas funcionalidades
- `fix:` Corrección de bugs
- `docs:` Cambios en documentación
- `style:` Cambios de formato/estilo
- `refactor:` Refactorización de código

### Workflow de Desarrollo
1. Fork del repositorio
2. Crear branch feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'feat: agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📈 Roadmap Futuro

### Funcionalidades Planificadas
- [ ] **Notificaciones Push**: Sistema de recordatorios automáticos
- [ ] **Exportación de Datos**: PDF/Excel de horarios y tareas
- [ ] **Modo Offline**: Funcionalidad básica sin conexión
- [ ] **API RESTful Completa**: Endpoints para integración externa
- [ ] **Dashboard Analytics**: Estadísticas de productividad
- [ ] **Temas Personalizables**: Modo oscuro/claro y colores personalizados
- [ ] **Mobile App**: Aplicación móvil híbrida
- [ ] **Integración Calendarios**: Google Calendar, Outlook, etc.

### Mejoras Técnicas
- [ ] **Tests Automatizados**: Suite completa de pruebas unitarias
- [ ] **CI/CD Pipeline**: Automatización de deployment
- [ ] **Docker**: Containerización completa
- [ ] **Redis Cache**: Optimización de rendimiento
- [ ] **WebSockets**: Actualizaciones en tiempo real
- [ ] **Microservicios**: Separación de funcionalidades

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Novato22y** - Desarrollo principal - [GitHub](https://github.com/Novato22y)

## 🙏 Agradecimientos

- Comunidad Flask por la excelente documentación
- Google por las herramientas OAuth 2.0
- Contribuidores de las librerías open source utilizadas

---

**📧 Contacto**: Para soporte o preguntas, abre un issue en el repositorio de GitHub.

**🌟 ¡Star el proyecto si te fue útil!**