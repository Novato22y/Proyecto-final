# School Planner - Estructura Modular

## 📁 Nueva Estructura del Proyecto

El proyecto ha sido reorganizado en módulos separados para facilitar el mantenimiento y desarrollo:

### **Archivos Principales:**

- **`app_new.py`** - Aplicación principal Flask (versión simplificada)
- **`app.py`** - Archivo original (mantener como respaldo)

### **Módulos Separados:**

#### **1. `config.py`** - Configuraciones
- Configuración de Flask (SECRET_KEY, DEBUG, etc.)
- Configuración de la base de datos PostgreSQL
- Configuración de la aplicación (HOST, PORT)

#### **2. `database.py`** - Base de Datos
- Conexión a PostgreSQL
- Creación de tablas
- Funciones CRUD para todas las entidades
- Validaciones de base de datos

#### **3. `models.py`** - Modelos de Datos
- Clase `User` con métodos estáticos
- Autenticación y autorización
- Gestión de usuarios

#### **4. `routes.py`** - Rutas de la Aplicación
- Todas las rutas HTTP organizadas por funcionalidad
- Autenticación requerida donde sea necesario
- Manejo de errores y respuestas JSON

#### **5. `utils.py`** - Funciones Utilitarias
- Creación del usuario administrador
- Inicialización de la base de datos
- Funciones auxiliares

## 🚀 Cómo Usar la Nueva Estructura

### **Para Desarrollo:**
```bash
# Usar la nueva aplicación modular
python app_new.py
```

### **Para Producción:**
```bash
# Usar la aplicación original
python app.py
```

## 🔧 Ventajas de la Nueva Estructura

### **✅ Beneficios:**
1. **Mantenibilidad** - Código más fácil de mantener y actualizar
2. **Legibilidad** - Cada archivo tiene una responsabilidad específica
3. **Reutilización** - Módulos pueden ser reutilizados en otros proyectos
4. **Testing** - Más fácil escribir pruebas unitarias
5. **Colaboración** - Múltiples desarrolladores pueden trabajar en diferentes módulos
6. **Debugging** - Más fácil encontrar y corregir errores

### **📋 Organización por Funcionalidad:**
- **Configuración** → `config.py`
- **Base de Datos** → `database.py`
- **Modelos** → `models.py`
- **Rutas** → `routes.py`
- **Utilidades** → `utils.py`
- **Aplicación** → `app_new.py`

## 🔄 Migración

### **Paso a Paso:**
1. **Verificar dependencias** - Asegurarse de que todas las dependencias estén instaladas
2. **Probar nueva aplicación** - Ejecutar `python app_new.py`
3. **Verificar funcionalidad** - Comprobar que todas las funciones trabajen correctamente
4. **Reemplazar archivo original** - Una vez verificado, reemplazar `app.py` con `app_new.py`

### **Dependencias Requeridas:**
```bash
pip install -r requirements.txt
```

## 🐛 Solución de Problemas

### **Error de Importación:**
Si hay errores de importación, verificar que:
- Todos los archivos estén en el mismo directorio
- Las dependencias estén instaladas correctamente
- No haya conflictos de nombres de archivos

### **Error de Base de Datos:**
Si hay errores de base de datos, verificar:
- Configuración en `config.py`
- Conexión a PostgreSQL
- Permisos de usuario

## 📝 Notas Importantes

- **Mantener respaldo** del archivo `app.py` original
- **Probar exhaustivamente** antes de usar en producción
- **Documentar cambios** en cada módulo
- **Versionar cambios** usando control de versiones

## 🎯 Próximos Pasos

1. **Probar la nueva estructura** con `app_new.py`
2. **Verificar todas las funcionalidades**
3. **Optimizar código** si es necesario
4. **Implementar tests** para cada módulo
5. **Documentar API** si se planea usar como servicio
