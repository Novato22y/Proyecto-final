# 📚 Planeador Escolar - Proyecto Final

## 🎯 **Descripción del Proyecto**

Planeador Escolar es una aplicación web desarrollada en **Flask** que permite a los estudiantes organizar su horario semanal, gestionar materias, tareas, exámenes y notas de manera eficiente.

## 🏗️ **Arquitectura del Proyecto**

Este proyecto ha sido reorganizado siguiendo las **mejores prácticas de Flask** para hacerlo más modular, mantenible y escalable.

### 📁 **Estructura de Directorios**

```
Proyecto-final/
├── app/                          # 🎯 Paquete principal de la aplicación
│   ├── __init__.py              # 🏭 Factory de la aplicación Flask
│   ├── models.py                # 👤 Modelos de datos (User, etc.)
│   ├── database.py              # 🗄️ Operaciones de base de datos
│   └── routes.py                # 🛣️ Rutas y vistas (organizadas en blueprints)
├── static/                       # 🎨 Archivos estáticos (CSS, JS, imágenes)
│   ├── css/
│   │   ├── styles.css           # 🎨 Estilos principales
│   │   ├── auth.css             # 🔐 Estilos de autenticación
│   │   └── base.css             # 🏗️ Estilos base
│   ├── js/
│   │   └── script.js            # ⚡ Funcionalidades JavaScript
│   └── images/                  # 🖼️ Imágenes de la aplicación
├── templates/                    # 📄 Plantillas HTML
│   ├── index.html               # 🏠 Página principal
│   ├── login.html               # 🔑 Página de inicio de sesión
│   ├── register.html            # 📝 Página de registro
│   └── subject_detail.html      # 📚 Detalle de materia
├── config.py                    # ⚙️ Configuración de la aplicación
├── run.py                       # 🚀 Punto de entrada principal
├── requirements.txt             # 📦 Dependencias del proyecto
└── README.md                    # 📖 Este archivo
```

## 🚀 **Características Principales**

### 🔐 **Sistema de Autenticación**
- **Registro de usuarios** con nombre, email y contraseña
- **Inicio de sesión** seguro con Flask-Login
- **Gestión de sesiones** persistentes

### 📅 **Gestión del Horario**
- **Horario semanal** (Lunes a Viernes)
- **Agregar/eliminar materias** por día y hora
- **Ordenamiento automático** por hora
- **Edición en tiempo real** de materias

### 📚 **Gestión de Materias**
- **Crear materias** personalizadas
- **Eliminar materias** con confirmación
- **Vista detallada** de cada materia

### ✅ **Sistema de Tareas**
- **Crear tareas** con descripción y fecha límite
- **Marcar como completadas** ✅
- **Eliminar tareas** existentes

### 📝 **Sistema de Exámenes**
- **Registrar exámenes** con tema y fecha
- **Agregar notas** después del examen
- **Historial completo** de evaluaciones

### 📖 **Sistema de Notas**
- **Crear notas** de estudio
- **Fecha de creación** automática
- **Edición y eliminación** de notas

## 🛠️ **Tecnologías Utilizadas**

- **Backend**: Python 3.x + Flask 3.1.1
- **Base de Datos**: PostgreSQL + psycopg2
- **Autenticación**: Flask-Login
- **Frontend**: HTML5 + CSS3 + JavaScript ES6+
- **Templates**: Jinja2
- **Seguridad**: Werkzeug (hashing de contraseñas)

## 📋 **Requisitos del Sistema**

- **Python**: 3.8 o superior
- **PostgreSQL**: 12 o superior
- **Navegador**: Chrome, Firefox, Safari, Edge (moderno)

## 🚀 **Instalación y Configuración**

### **1. Clonar el Repositorio**
```bash
git clone <url-del-repositorio>
cd Proyecto-final
```

### **2. Crear Entorno Virtual**
```bash
# Windows
python -m venv venv
venv\Scripts\activate.bat

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Base de Datos**
1. Crear base de datos PostgreSQL: `planeador_escolar`
2. Actualizar credenciales en `config.py`
3. Ejecutar la aplicación para crear tablas automáticamente

### **5. Ejecutar la Aplicación**
```bash
python run.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

## 🔧 **Configuración de la Base de Datos**

Edita `config.py` con tus credenciales:

```python
class Config:
    DB_HOST = "localhost"
    DB_NAME = "planeador_escolar"
    DB_USER = "tu_usuario"
    DB_PASSWORD = "tu_contraseña"
    DB_PORT = "5432"
```

## 📱 **Uso de la Aplicación**

### **1. Registro e Inicio de Sesión**
- Crear cuenta nueva o iniciar sesión existente
- Acceso seguro con email y contraseña

### **2. Gestión del Horario**
- Ver horario semanal organizado
- Agregar materias con botón "+"
- Editar materias haciendo clic en ellas
- Eliminar materias con botón 🗑️

### **3. Gestión de Materias**
- Crear materias desde la barra lateral
- Acceder al detalle de cada materia
- Gestionar tareas, exámenes y notas

### **4. Funcionalidades Avanzadas**
- **Reloj en tiempo real** en todas las páginas
- **Formularios dinámicos** que aparecen/desaparecen
- **Confirmaciones** antes de eliminar elementos
- **Validación** de formularios en tiempo real

## 🎨 **Personalización**

### **Estilos CSS**
- Modificar `static/css/styles.css` para cambios generales
- `static/css/auth.css` para páginas de autenticación
- `static/css/base.css` para estilos base

### **Funcionalidades JavaScript**
- Editar `static/js/script.js` para nuevas funcionalidades
- Funciones modulares organizadas por sección

### **Plantillas HTML**
- Modificar archivos en `templates/` para cambios de diseño
- Sistema de herencia de Jinja2 para consistencia

## 🔒 **Seguridad**

- **Hashing de contraseñas** con Werkzeug
- **Protección CSRF** automática
- **Validación de entrada** en todos los formularios
- **Sesiones seguras** con Flask-Login
- **Verificación de propiedad** de recursos

## 🧪 **Pruebas**

### **Probar Funcionalidades Básicas**
1. ✅ Registro de usuario nuevo
2. ✅ Inicio de sesión
3. ✅ Crear materia
4. ✅ Agregar horario
5. ✅ Crear tarea
6. ✅ Agregar examen
7. ✅ Crear nota

### **Verificar Base de Datos**
- Las tablas se crean automáticamente
- Usuario administrador se crea en primer uso
- Relaciones entre tablas funcionan correctamente

## 🐛 **Solución de Problemas**

### **Error de Conexión a Base de Datos**
- Verificar que PostgreSQL esté ejecutándose
- Confirmar credenciales en `config.py`
- Verificar que la base de datos exista

### **Error de Plantillas**
- Verificar que las plantillas estén en `templates/`
- Confirmar rutas en `url_for()` usen blueprints
- Verificar sintaxis Jinja2

### **Error de Archivos Estáticos**
- Verificar que archivos estén en `static/`
- Confirmar rutas en HTML usen `/static/`
- Verificar permisos de archivos

## 📈 **Mejoras Futuras**

- [ ] **Sistema de notificaciones** para tareas próximas
- [ ] **Calendario visual** mensual/anual
- [ ] **Exportar horario** a PDF/Excel
- [ ] **Sincronización** con calendarios externos
- [ ] **Temas visuales** personalizables
- [ ] **API REST** para integración móvil
- [ ] **Sistema de respaldo** automático
- [ ] **Estadísticas** de progreso académico

## 👥 **Contribución**

1. Fork del proyecto
2. Crear rama para nueva funcionalidad
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## 📄 **Licencia**

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 **Contacto**

- **Desarrollador**: [Tu Nombre]
- **Email**: [tu-email@ejemplo.com]
- **Proyecto**: Planeador Escolar v2.0

## 🙏 **Agradecimientos**

- **Flask** por el framework web
- **PostgreSQL** por la base de datos robusta
- **Comunidad Python** por el soporte continuo

---

**✨ ¡Disfruta organizando tu vida académica con el Planeador Escolar! ✨**