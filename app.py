from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime # Necesario para la marca de tiempo en notes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here' # ¡CAMBIA ESTO POR UNA CLAVE SEGURA!

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Especifica la ruta para el login

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    # Método necesario para Flask-Login para cargar un usuario por su ID
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
                user_data = cur.fetchone()
                if user_data:
                    return User(id=user_data[0], name=user_data[1], email=user_data[2], role=user_data[3])
                return None
            except psycopg2.Error as e:
                print(f"Error loading user {user_id}: {e}")
                return None
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return None

# Configuración de la base de datos (REEMPLAZA CON TUS PROPIOS VALORES)
DB_HOST = "localhost"
DB_NAME = "planeador_escolar"
DB_USER = "postgres"
DB_PASSWORD = "MmateomunozV1.0"
DB_PORT = "5432"  # Puerto predeterminado de PostgreSQL

def get_db_connection():
    """Establece una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            options=f"-c client_encoding=UTF8"  # Agrega esta línea
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def create_table():
    """Crea las tablas necesarias si no existen y añade la columna user_id."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Crear tabla de usuarios
            print("Intentando crear tabla 'users'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL DEFAULT 'cliente'
                )
            """)
            print("Tabla 'users' verificada/creada.")

            print("Intentando crear tabla 'schedule'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schedule (
                    id SERIAL PRIMARY KEY, -- Añadir ID para clave primaria si no existe
                    day VARCHAR(20) NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    subject VARCHAR(100),
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Añadir columna user_id
                    UNIQUE(day, time, user_id) -- Añadir restricción UNIQUE compuesta si aplica al horario
                )
            """)
            print("Tabla 'schedule' verificada/creada.")

            print("Intentando crear tabla 'materias'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS materias (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, -- Añadir columna user_id
                    UNIQUE(name, user_id) -- Restricción única para la combinación de nombre y user_id
                )
            """)
            print("Tabla 'materias' verificada/creada.")

            print("Intentando crear tabla 'tasks'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    description TEXT NOT NULL,
                    due_date DATE,
                    completed BOOLEAN DEFAULT FALSE,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE -- Añadir columna user_id
                )
            """)
            print("Tabla 'tasks' verificada/creada.")

            print("Intentando crear tabla 'exams'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    topic VARCHAR(255) NOT NULL,
                    exam_date DATE,
                    grade NUMERIC(5, 2),
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE -- Añadir columna user_id
                )
            """)
            print("Tabla 'exams' verificada/creada.")

            print("Intentando crear tabla 'notes'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE -- Añadir columna user_id
                )
            """)
            print("Tabla 'notes' verificada/creada.")

            conn.commit()
            print("Todas las tablas verificadas o creadas correctamente.")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error detallado al crear tabla: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


def load_schedule(user_id): # <-- Añadido user_id como argumento
    """Carga el horario para un usuario específico desde la base de datos."""
    conn = get_db_connection()
    schedule = {}
    if conn:
        cur = conn.cursor()
        try:
            # Modificada la consulta para filtrar por user_id
            cur.execute("SELECT day, time, subject FROM schedule WHERE user_id = %s", (user_id,))
            rows = cur.fetchall()
            for row in rows:
                day, time, subject = row
                if day not in schedule:
                    schedule[day] = {}
                schedule[day][time] = subject
        except psycopg2.Error as e:
            print(f"Error al cargar el horario: {e}")
        finally:
            cur.close()
            conn.close()

    # Ordenar las materias por hora
    for day in schedule:
        schedule[day] = dict(sorted([(time, subject) for time, subject in schedule[day].items()], key=lambda item: item[0]))

    return schedule

def load_materias(user_id): # <-- Añadido user_id como argumento
    """Carga las materias para un usuario específico desde la base de datos."""
    conn = get_db_connection()
    materias = []
    if conn:
        cur = conn.cursor()
        try:
            # Modificada la consulta para filtrar por user_id
            cur.execute("SELECT id, name FROM materias WHERE user_id = %s", (user_id,))
            rows = cur.fetchall()
            for row in rows:
                materia_id, name = row
                materias.append({'id': materia_id, 'name': name})
        except psycopg2.Error as e:
            print(f"Error al cargar las materias: {e}")
        finally:
            cur.close()
            conn.close()
    return materias

def save_schedule(day, time, subject, user_id):
    """Guarda o actualiza una materia en el horario para un usuario específico en la base de datos."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Intenta actualizar si ya existe para este usuario
            cur.execute("UPDATE schedule SET subject = %s WHERE day = %s AND time = %s AND user_id = %s", (subject, day, time, user_id))
            if cur.rowcount == 0:
                # Si no existe para este usuario, inserta
                cur.execute("INSERT INTO schedule (day, time, subject, user_id) VALUES (%s, %s, %s, %s)", (day, time, subject, user_id))
            conn.commit()
            print(f"Horario guardado/actualizado para {day} a las {time} para usuario {user_id}: {subject}")
        except psycopg2.Error as e:
            print(f"Error al guardar el horario: {e}")
        finally:
            cur.close()
            conn.close()

def delete_schedule(day, time):
    """Elimina una materia de la base de datos."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM schedule WHERE day = %s AND time = %s", (day, time))
            conn.commit()
            print(f"Materia eliminada para {day} a las {time}")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar la materia: {e}")
            return False
        finally:
            cur.close()
            conn.close()

def get_materia_details(materia_id):
    """Carga los detalles de una materia por su ID, incluyendo tareas, exámenes y notas."""
    conn = get_db_connection()
    materia_details = None
    if conn:
        cur = conn.cursor()
        try:
            # Obtener el nombre de la materia
            cur.execute("SELECT id, name FROM materias WHERE id = %s", (materia_id,))
            materia_row = cur.fetchone()
            if materia_row:
                materia_details = {
                    'id': materia_row[0],
                    'name': materia_row[1],
                    'tasks': [],
                    'exams': [],
                    'notes': []
                }

                # Obtener las tareas de la materia
                cur.execute("SELECT id, description, due_date, completed FROM tasks WHERE materia_id = %s ORDER BY due_date", (materia_id,))
                tasks_rows = cur.fetchall()
                for task in tasks_rows:
                    materia_details['tasks'].append({'id': task[0], 'description': task[1], 'due_date': task[2], 'completed': task[3]})

                # Obtener los exámenes de la materia
                cur.execute("SELECT id, topic, exam_date, grade FROM exams WHERE materia_id = %s ORDER BY exam_date", (materia_id,))
                exams_rows = cur.fetchall()
                for exam in exams_rows:
                    materia_details['exams'].append({'id': exam[0], 'topic': exam[1], 'exam_date': exam[2], 'grade': exam[3]})

                # Obtener las notas de la materia
                cur.execute("SELECT id, content FROM notes WHERE materia_id = %s", (materia_id,))
                notes_rows = cur.fetchall()
                for note in notes_rows:
                    materia_details['notes'].append({'id': note[0], 'content': note[1]})

        except psycopg2.Error as e:
            print(f"Error al cargar detalles de la materia {materia_id}: {e}")
        finally:
            cur.close()
            conn.close()

    return materia_details

# --- Nuevas rutas para registro y login ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated: # Si el usuario ya está logeado, redirigir
        return redirect(url_for('principal'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = 'cliente' # Por defecto, solo se registran clientes

        if not name or not email or not password:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('register.html')

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Verificar si el correo ya existe
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                existing_user = cur.fetchone()
                if existing_user:
                    flash('El correo electrónico ya está registrado.', 'danger')
                    return render_template('register.html')

                # Hashear la contraseña antes de guardarla
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                # Insertar nuevo usuario
                cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)", (name, email, hashed_password, role))
                conn.commit()
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al registrar usuario: {e}")
                flash('Ocurrió un error durante el registro.', 'danger')
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # Si el usuario ya está logeado, redirigir
        return redirect(url_for('principal'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor, ingresa correo y contraseña.', 'warning')
            return render_template('login.html')

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
                user_data = cur.fetchone()

                if user_data and check_password_hash(user_data[3], password): # user_data[3] es la contraseña hasheada
                    user = User(id=user_data[0], name=user_data[1], email=user_data[2], role=user_data[4])
                    login_user(user)
                    print(f"Usuario logeado: {user.name} ({user.email}) con rol {user.role}")
                    # Redirigir a la página principal o a la página solicitada
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('principal'))
                else:
                    flash('Correo electrónico o contraseña incorrectos.', 'danger')
            except psycopg2.Error as e:
                print(f"Error al intentar login: {e}")
                flash('Ocurrió un error al intentar iniciar sesión.', 'danger')
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

    return render_template('login.html')

@app.route('/logout')
@login_required # Solo usuarios logeados pueden hacer logout
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('principal'))

@app.route('/')
def principal():
    create_table()  # Asegúrate de que las tablas existan

    schedule = {}
    materias = []

    if current_user.is_authenticated:
        # Cargar datos solo para el usuario logeado
        schedule = load_schedule(current_user.id)  # <-- Añadido current_user.id
        materias = load_materias(current_user.id) 

    # Pasar current_user a la plantilla para mostrar el nombre o el enlace de login/registro
    return render_template("index.html", schedule=schedule, materias=materias, current_user=current_user)

@app.route('/save_schedule', methods=['POST'])
def save_schedule_route():
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')
    if day and time and subject is not None:
        save_schedule(day, time, subject, current_user.id)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

@app.route('/add_schedule', methods=['POST'])
@login_required # <-- Asegurar que el usuario esté logeado
def add_schedule_route():
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')

    if day and time and subject and current_user.is_authenticated: # <-- Verificar autenticación
        save_schedule(day, time, subject, current_user.id) # <-- Pasar current_user.id
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400 # <-- Mensaje de error más específico

@app.route('/delete_schedule', methods=['POST'])
def delete_schedule_route():
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    if day and time:
        if delete_schedule(day, time):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Error al eliminar la materia'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

# Nueva ruta para agregar materias
@app.route('/add_materia', methods=['POST'])
@login_required # <-- Asegurar que el usuario esté logeado
def add_materia_route():
    data = request.get_json()
    materia_name = data.get('name')

    if materia_name and current_user.is_authenticated: # <-- Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Insertar la nueva materia y obtener su ID, asociándola al user_id logeado
                cur.execute("INSERT INTO materias (name, user_id) VALUES (%s, %s) RETURNING id;", (materia_name, current_user.id)) # <-- Añadido user_id
                materia_id = cur.fetchone()[0]
                conn.commit()
                print(f"Materia agregada: {materia_name} con ID {materia_id} para usuario {current_user.id}") # <-- Añadido user_id en log
                return jsonify({'status': 'success', 'materia_id': materia_id})
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                print(f"Error: La materia '{materia_name}' ya existe.")
                return jsonify({'status': 'error', 'message': 'La materia ya existe.'}), 400
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al agregar la materia: {e}")
                return jsonify({'status': 'error', 'message': 'Error al agregar la materia'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Nombre de materia no proporcionado'}), 400

# Nueva ruta para eliminar materias
@app.route('/delete_materia', methods=['POST'])
def delete_materia_route():
    data = request.get_json()
    materia_id = data.get('materia_id')

    if materia_id is not None:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Eliminar la materia por su ID
                cur.execute("DELETE FROM materias WHERE id = %s", (materia_id,))
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Materia eliminada con ID: {materia_id}")
                    return jsonify({'status': 'success'})
                else:
                    print(f"Error al eliminar materia: No se encontró materia con ID {materia_id}")
                    return jsonify({'status': 'error', 'message': 'Materia no encontrada'}), 404
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al eliminar la materia: {e}")
                return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar la materia'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'ID de materia no proporcionado'}), 400

# Nueva ruta para la página de detalle de la materia
@app.route('/materia/<int:materia_id>')
def materia_detalle(materia_id):
    materia_details = get_materia_details(materia_id)
    if materia_details:
        return render_template('subject_detail.html', materia=materia_details)
    else:
        return "Materia no encontrada", 404 # O renderizar una plantilla de error

# Rutas para agregar Tareas, Exámenes y Notas
@app.route('/add_task', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def add_task_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    description = data.get('description')
    due_date = data.get('due_date') # Puede ser None

    # Verificar que la materia pertenezca al usuario logeado antes de agregar la tarea
    if materia_id is not None and description and current_user.is_authenticated:
        if not is_materia_owned_by_user(materia_id, current_user.id):
            return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Insertar la nueva tarea, asociándola al user_id logeado
                cur.execute("INSERT INTO tasks (materia_id, description, due_date, user_id) VALUES (%s, %s, %s, %s) RETURNING id;", (materia_id, description, due_date, current_user.id)) # <-- Añadido user_id
                task_id = cur.fetchone()[0]
                conn.commit()
                print(f"Tarea agregada para materia {materia_id} con ID {task_id} para usuario {current_user.id}")
                return jsonify({'status': 'success', 'task_id': task_id})
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al agregar la tarea: {e}")
                return jsonify({'status': 'error', 'message': 'Error al agregar la tarea'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para la tarea'}), 400

@app.route('/add_exam', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def add_exam_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    topic = data.get('topic')
    exam_date_str = data.get('exam_date') # Obtener la fecha como string inicialmente
    grade = data.get('grade') # Puede ser None

    # Validar que la materia pertenezca al usuario logeado
    if materia_id is None or not topic or not current_user.is_authenticated:
         return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400

    if not is_materia_owned_by_user(materia_id, current_user.id):
        return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

    # --- Validación de Fecha ---
    exam_date = None # Inicializar como None
    if exam_date_str:
        try:
            # Intentar parsear la fecha del string al formato DATE de la base de datos
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date() # Usar .date() para obtener solo la fecha
        except ValueError:
            # Si el formato de fecha es inválido
            return jsonify({'status': 'error', 'message': 'Formato de fecha de examen inválido. Use YYYY-MM-DD.'}), 400
    # --------------------------

    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Insertar el nuevo examen, asociándola al user_id logeado con la fecha validada
            cur.execute("INSERT INTO exams (materia_id, topic, exam_date, grade, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;", (materia_id, topic, exam_date, grade, current_user.id))
            exam_id = cur.fetchone()[0]
            conn.commit()
            print(f"Examen agregado para materia {materia_id} con ID {exam_id} para usuario {current_user.id}")
            return jsonify({'status': 'success', 'exam_id': exam_id})
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al agregar el examen: {e}")
            return jsonify({'status': 'error', 'message': 'Error al agregar el examen'}), 500
        finally:
            cur.close()
            conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Error al conectar a la base de datos'}), 500

@app.route('/add_note', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def add_note_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    content = data.get('content')

    # Verificar que la materia pertenezca al usuario logeado antes de agregar la nota
    if materia_id is not None and content and current_user.is_authenticated:
        if not is_materia_owned_by_user(materia_id, current_user.id):
             return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                print(f"Intentando agregar nota para materia_id: {materia_id}, contenido: {content[:50]}... para usuario {current_user.id}") # Log de diagnóstico
                # Insertar la nueva nota, asociándola al user_id logeado
                cur.execute("INSERT INTO notes (materia_id, content, user_id) VALUES (%s, %s, %s) RETURNING id, created_at;", (materia_id, content, current_user.id)) # <-- Añadido user_id
                note_id, created_at = cur.fetchone()
                conn.commit()
                print(f"Nota agregada para materia {materia_id} con ID {note_id}")
                # Devolver también la fecha de creación para mostrar en el frontend
                return jsonify({'status': 'success', 'note_id': note_id, 'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')}) # Formato de fecha/hora
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al agregar la nota: {e}")
                return jsonify({'status': 'error', 'message': 'Error al agregar la nota'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para la nota'}), 400

# Rutas para eliminar Tareas, Exámenes y Notas
@app.route('/delete_task', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def delete_task_route():
    data = request.get_json()
    task_id = data.get('task_id')

    if task_id is not None and current_user.is_authenticated: # Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Eliminar la tarea por su ID Y user_id
                cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, current_user.id)) # <-- Añadido user_id
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Tarea eliminada con ID: {task_id}")
                    return jsonify({'status': 'success'})
                else:
                    print(f"Error al eliminar tarea: No se encontró tarea con ID {task_id}")
                    return jsonify({'status': 'error', 'message': 'Tarea no encontrada'}), 404
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al eliminar la tarea: {e}")
                return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar la tarea'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'ID de tarea no proporcionado'}), 400

@app.route('/delete_exam', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def delete_exam_route():
    data = request.get_json()
    exam_id = data.get('exam_id')

    if exam_id is not None and current_user.is_authenticated: # Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Eliminar el examen por su ID Y user_id
                cur.execute("DELETE FROM exams WHERE id = %s AND user_id = %s", (exam_id, current_user.id)) # <-- Añadido user_id
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Examen eliminado con ID: {exam_id}")
                    return jsonify({'status': 'success'})
                else:
                    print(f"Error al eliminar examen: No se encontró examen con ID {exam_id}")
                    return jsonify({'status': 'error', 'message': 'Examen no encontrado'}), 404
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al eliminar el examen: {e}")
                return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar el examen'}), 500
            finally:
                cur.close()
                conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado'}), 400

@app.route('/delete_note', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def delete_note_route():
    data = request.get_json()
    note_id = data.get('note_id')

    if note_id is not None and current_user.is_authenticated: # Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Eliminar la nota por su ID Y user_id
                cur.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, current_user.id)) # <-- Añadido user_id
                conn.commit()
                if cur.rowcount > 0:
                    print(f"Nota eliminada con ID: {note_id}")
                    return jsonify({'status': 'success'})
                else:
                    print(f"Error al eliminar nota: No se encontró nota con ID {note_id}")
                    return jsonify({'status': 'error', 'message': 'Nota no encontrada'}), 404
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al eliminar la nota: {e}")
                return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar la nota'}), 500
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'ID de nota no proporcionado'}), 400

# Nuevas rutas para guardar/actualizar elementos

@app.route('/save_task', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def save_task_route():
    data = request.get_json()
    task_id = data.get('task_id')
    description = data.get('description') # Opcional: también permitir editar fecha y completado?

    if task_id is not None and description is not None and current_user.is_authenticated: # Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Actualizar la tarea por su ID Y user_id
                cur.execute("UPDATE tasks SET description = %s WHERE id = %s AND user_id = %s", (description, task_id, current_user.id)) # <-- Añadido user_id
                conn.commit()
                print(f"Tarea {task_id} actualizada.")
                return jsonify({'status': 'success'})
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al actualizar tarea {task_id}: {e}")
                return jsonify({'status': 'error', 'message': 'Error al actualizar tarea'}), 500
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para actualizar tarea'}), 400

@app.route('/save_exam', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def save_exam_route():
    data = request.get_json()
    exam_id = data.get('exam_id')
    topic = data.get('topic')
    grade = data.get('grade') # Podría ser None
    exam_date_str = data.get('exam_date') # Obtener la fecha como string inicialmente, si se envía

    if exam_id is None or not current_user.is_authenticated: # Verificar autenticación y ID
         return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado o usuario no autenticado'}), 400

    # --- Validación de Fecha (si se proporciona) ---
    exam_date = None # Inicializar como None
    if exam_date_str is not None: # Verificar si el campo de fecha fue enviado en el JSON
        if exam_date_str == '': # Si se envió vacío, setear a NULL
            exam_date = None
        else:
            try:
                # Intentar parsear la fecha del string
                exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date() # Usar .date()
            except ValueError:
                # Si el formato de fecha es inválido
                return jsonify({'status': 'error', 'message': 'Formato de fecha de examen inválido. Use YYYY-MM-DD.'}), 400
    # ------------------------------------------

    conn = get_db_connection()
    if conn:
         cur = conn.cursor()
         try:
             update_fields = []
             update_values = []
             if topic is not None: # Si se proporciona el campo topic
                 update_fields.append("topic = %s")
                 update_values.append(topic)

             if 'grade' in data: # Verificar si el campo grade fue enviado (incluso si es None)
                  update_fields.append("grade = %s")
                  update_values.append(grade) # grade ya es None o el valor numérico

             if exam_date_str is not None: # Si el campo exam_date fue enviado (válido o None)
                 update_fields.append("exam_date = %s")
                 update_values.append(exam_date)

             if not update_fields:
                 return jsonify({'status': 'error', 'message': 'No hay campos para actualizar'}), 400

             # La última parte del WHERE clause es el ID del examen Y user_id
             update_values.append(exam_id)
             update_values.append(current_user.id)

             # Ajustar la consulta dinámicamente
             query = f"UPDATE exams SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"

             cur.execute(query, update_values)
             conn.commit()
             print(f"Examen {exam_id} actualizado.")
             return jsonify({'status': 'success'})
         except psycopg2.Error as e:
             conn.rollback()
             print(f"Error al actualizar examen {exam_id}: {e}")
             return jsonify({'status': 'error', 'message': 'Error al actualizar examen'}), 500
         finally:
             if cur:
                 cur.close()
             if conn:
                 conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Error al conectar a la base de datos'}), 500

@app.route('/save_note', methods=['POST'])
@login_required # Asegurar que el usuario esté logeado
def save_note_route():
    data = request.get_json()
    note_id = data.get('note_id')
    content = data.get('content')

    if note_id is not None and content is not None and current_user.is_authenticated: # Verificar autenticación
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Actualizar la nota por su ID Y user_id
                cur.execute("UPDATE notes SET content = %s WHERE id = %s AND user_id = %s", (content, note_id, current_user.id)) # <-- Añadido user_id
                conn.commit()
                print(f"Nota {note_id} actualizada.")
                return jsonify({'status': 'success'})
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Error al actualizar nota {note_id}: {e}")
                return jsonify({'status': 'error', 'message': 'Error al actualizar nota'}), 500
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para actualizar nota'}), 400

def is_materia_owned_by_user(materia_id, user_id):
    """Verifica si una materia pertenece a un usuario dado."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT 1 FROM materias WHERE id = %s AND user_id = %s", (materia_id, user_id))
            result = cur.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f"Error verifying materia ownership: {e}")
            return False
        finally:
            if cur: # Asegurarse de que el cursor se cierre incluso si hay un error
                cur.close()
            if conn: # Asegurarse de que la conexión se cierre
                conn.close()

if __name__ == '__main__':
    app.run(debug=True)

# --- Función para crear el usuario administrador (ejecutar una vez) ---
def create_admin_user():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Verificar si el administrador ya existe por correo electrónico
            admin_email = 'admin@planeador.com' # Correo del administrador
            cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
            existing_admin = cur.fetchone()

            if existing_admin:
                print("El usuario administrador ya existe.")
                return # No hacer nada si ya existe

            # Crear contraseña hasheada para el administrador
            admin_password_raw = 'admin_password_segura_123' # ¡CAMBIA ESTO POR UNA CONTRASEÑA FUERTE!
            hashed_admin_password = generate_password_hash(admin_password_raw, method='pbkdf2:sha256')

            # Insertar el usuario administrador
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
                        ('Administrador', admin_email, hashed_admin_password, 'administrador'))
            admin_id = cur.fetchone()[0]
            conn.commit()
            print("\n") # Nueva línea para mejor formato
            print("----------------------------------------------------")
            print("¡Usuario administrador creado exitosamente!")
            print(f"ID: {admin_id}")
            print(f"Nombre: Administrador")
            print(f"Correo: {admin_email}")
            print(f"Contraseña (plano, ¡CÁMBIALA INMEDIATAMENTE!): {admin_password_raw}")
            print(f"Rol: administrador")
            print("----------------------------------------------------")
            print("\n")
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al crear el usuario administrador: {e}")
        finally:
            if cur: # Asegurarse de que el cursor se cierre incluso si hay un error
                cur.close()
            if conn: # Asegurarse de que la conexión se cierre
                    conn.close()

# --- Llamar a create_table y create_admin_user al inicio ---
# Asegurarse de que las tablas se creen y el admin se añada la primera vez
with app.app_context(): # Ejecutar dentro del contexto de la aplicación Flask
    create_table()
    create_admin_user()
