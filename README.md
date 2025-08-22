# School Planner

Este proyecto es un planeador escolar simple desarrollado con Flask (Python) para el backend y HTML, CSS y JavaScript para el frontend. Permite a los usuarios gestionar su horario semanal, materias, tareas, exámenes y notas, con datos separados por cuenta de usuario.

## Características Principales

*   **Horario Semanal:** Visualización y gestión interactiva del horario.
*   **Gestión de Materias:** Añade, visualiza y elimina materias. Cada materia tiene su propia página de detalle.
*   **Detalles de Materia:** En la página de detalle de cada materia, los usuarios pueden gestionar Tareas, Exámenes y Notas asociadas a esa materia específica.
*   **Sistema de Autenticación:
    *   **Registro:** Los nuevos usuarios pueden crear una cuenta (con rol 'cliente' por defecto).
    *   **Inicio/Cierre de Sesión:** Usuarios registrados pueden iniciar y cerrar sesión para acceder a sus datos.
*   **Gestión Básica de Usuarios:** El sistema soporta roles (administrador, trabajador, cliente). Se crea una cuenta de administrador por defecto al inicializar la base de datos.
*   **Separación de Datos por Usuario:** Todos los datos (horario, materias, tareas, exámenes, notas) están asociados a la cuenta del usuario que los crea, asegurando la privacidad y organización individual.
*   **Persistencia de Datos:** Los datos se guardan en una base de datos PostgreSQL.

## Configuración del Entorno

1.  **Clonar el repositorio** o tener los archivos del proyecto.

2.  **Instalar Python** y **pip** si no los tienes.

3.  **Crear un entorno virtual** (recomendado):
    ```bash
    python -m venv venv
    ```

4.  **Activar el entorno virtual**:
    *   En Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   En macOS y Linux:
        ```bash
        source venv/bin/activate
        ```

5.  **Instalar las dependencias de Python**:
    Crea o verifica que tienes un archivo `requirements.txt` con el siguiente contenido:
    ```
    Flask==2.3.3
    psycopg2-binary==2.9.9
    Flask-Login==0.6.3 # Añadido
    Werkzeug==2.3.8 # Añadido (necesario para generate_password_hash)
    ```
    Luego instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

6.  **Configurar la Base de Datos PostgreSQL**:
    *   Asegúrate de tener un servidor PostgreSQL instalado y ejecutándose.
    *   Crea una nueva base de datos (ej: `planeador_escolar`).
    *   Crea un usuario de base de datos y asigna una contraseña.
    *   **Actualiza la configuración de la base de datos en `app.py`** (busca la sección de `DB_HOST`, `DB_NAME`, etc.) con los detalles de tu configuración local.

## Ejecutar la Aplicación

1.  Asegúrate de que tu entorno virtual esté activado.
2.  Asegúrate de que tu servidor PostgreSQL esté ejecutándose.
3.  **Importante: Inicialización de la Base de Datos**
    *   Si es la primera vez que ejecutas la aplicación o si has tenido problemas con la estructura de las tablas, **elimina las tablas existentes** en tu base de datos usando un cliente de PostgreSQL (pgAdmin, psql, etc.). Puedes usar los siguientes comandos:
        ```sql
        DROP TABLE schedule CASCADE;
        DROP TABLE materias CASCADE;
        DROP TABLE tasks CASCADE;
        DROP TABLE exams CASCADE;
        DROP TABLE notes CASCADE;
        DROP TABLE users CASCADE;
        ```
    *   Luego, ejecuta la aplicación.
4.  Desde la raíz del proyecto, ejecuta el archivo `app.py`:
    ```bash
    python app.py
    ```
5.  Abre tu navegador y navega a `http://127.0.0.1:5000/` para acceder a la aplicación.

    *La primera vez que se ejecuta `app.py` con las tablas eliminadas, la función `create_table` se ejecutará para crear la estructura de la base de datos y se creará una cuenta de administrador por defecto.* Revisa la consola de Flask para las credenciales del administrador.

## Funcionalidad de Autenticación y Usuarios

*   **Página de Registro (`/register`):** Permite a los nuevos usuarios crear una cuenta proporcionando nombre, correo electrónico y contraseña.
*   **Página de Inicio de Sesión (`/login`):** Permite a los usuarios registrados acceder a sus cuentas.
*   **Página de Cierre de Sesión (`/logout`):** Cierra la sesión del usuario actual.
*   **Separación de Datos:** Al iniciar sesión, la aplicación carga y muestra solo los datos (horario, materias, etc.) asociados al usuario logeado. Al guardar o eliminar datos, estos se asocian o se filtran por el usuario actual.
*   **Cuenta de Administrador:** Una cuenta de administrador con credenciales por defecto se crea automáticamente la primera vez que las tablas se generan. Esta cuenta tiene rol 'administrador'.

## Estructura del Proyecto

```
./
├── app.py          # Backend de Flask, lógica de base de datos y rutas.
├── requirements.txt  # Dependencias de Python (Flask, psycopg2, Flask-Login, Werkzeug).
├── static/
│   ├── css/
│   │   ├── base.css # Estilos generales
│   │   ├── styles.css # Estilos principales (incluye index y subject_detail)
│   │   └── auth.css # Estilos para registro y login
│   ├── images/     # Imágenes utilizadas en el frontend.
│   └── js/
│       └── script.js # Lógica de frontend con JavaScript (manejo del DOM, peticiones AJAX).
└── templates/
    ├── index.html      # Página principal (horario, lista de materias).
    ├── subject_detail.html # Página de detalles de la materia (tareas, exámenes, notas).
    ├── register.html   # Página de registro de usuario.
    └── login.html      # Página de inicio de sesión.
```

## Posibles Problemas y Soluciones

*   **Errores de base de datos ("relation does not exist", etc.):** Si encuentras errores relacionados con tablas inexistentes o columnas faltantes después de realizar cambios en `create_table` en `app.py`, necesitarás **eliminar las tablas existentes** en tu base de datos manualmente (usando los comandos `DROP TABLE ... CASCADE;`) y luego reiniciar la aplicación. La aplicación recreará las tablas con la estructura actualizada al ejecutarse.
*   **Error `ValueError: year is out of range` al cargar detalles de materia:** Esto indica un dato de fecha inválido almacenado en la tabla `exams`. Debes identificar y eliminar/corregir el dato corrupto directamente en la base de datos usando SQL. Ejecuta una consulta `SELECT` en la tabla `exams` filtrando por `user_id` y `materia_id` para encontrar el dato problemático.
*   **Errores del linter en archivos HTML:** Las advertencias en los archivos HTML relacionadas con la sintaxis en atributos `onclick`/`onsubmit` que mezclan Jinja2 y JavaScript suelen ser "falsos positivos" visuales del linter y no afectan la funcionalidad si el código JavaScript está bien escrito.
*   **Problemas con la actualización visual del horario después de agregar:** Asegúrate de haber realizado la corrección manual en `static/js/script.js` dentro de la función `addSubjectToDOM` para usar variables JavaScript (`${variable}`) en lugar de sintaxis Jinja (`{{ variable }}`) al construir el HTML del nuevo elemento de lista.

## Autor

[Mateo Muñoz]