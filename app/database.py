# app/database.py - Funciones de conexión y operaciones con la base de datos
import psycopg2
from config import Config
from datetime import datetime

def get_db_connection():
    """Establece una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            options=f"-c client_encoding=UTF8"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def create_tables():
    """Crea las tablas necesarias si no existen."""
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

            # Crear tabla de horario
            print("Intentando crear tabla 'schedule'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schedule (
                    id SERIAL PRIMARY KEY,
                    day VARCHAR(20) NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    subject VARCHAR(100),
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(day, time, user_id)
                )
            """)
            print("Tabla 'schedule' verificada/creada.")

            # Crear tabla de materias
            print("Intentando crear tabla 'materias'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS materias (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(name, user_id)
                )
            """)
            print("Tabla 'materias' verificada/creada.")

            # Crear tabla de tareas
            print("Intentando crear tabla 'tasks'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    description TEXT NOT NULL,
                    due_date DATE,
                    completed BOOLEAN DEFAULT FALSE,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabla 'tasks' verificada/creada.")

            # Crear tabla de exámenes
            print("Intentando crear tabla 'exams'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    topic VARCHAR(255) NOT NULL,
                    exam_date DATE,
                    grade NUMERIC(5, 2),
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            print("Tabla 'exams' verificada/creada.")

            # Crear tabla de notas
            print("Intentando crear tabla 'notes'...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    materia_id INTEGER NOT NULL REFERENCES materias(id) ON DELETE CASCADE,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
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

def user_exists(email):
    """Verifica si un usuario ya existe por su email."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            result = cur.fetchone()
            return result is not None
        except psycopg2.Error as e:
            print(f"Error al verificar si el usuario existe: {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return False

def create_user(name, email, password, role='cliente'):
    """Crea un nuevo usuario en la base de datos."""
    from werkzeug.security import generate_password_hash
    
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Verificar si el usuario ya existe
            if user_exists(email):
                return None, "El correo electrónico ya está registrado."
            
            # Hashear la contraseña
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Insertar el nuevo usuario
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
                        (name, email, hashed_password, role))
            user_id = cur.fetchone()[0]
            conn.commit()
            
            print(f"Usuario creado exitosamente: {name} ({email}) con ID {user_id}")
            return user_id, None
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al crear usuario: {e}")
            return None, f"Error al crear el usuario: {e}"
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    return None, "Error de conexión a la base de datos"

def create_admin_user():
    """Crea el usuario administrador por defecto."""
    from werkzeug.security import generate_password_hash
    
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Verificar si el administrador ya existe
            admin_email = 'admin@planeador.com'
            cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
            existing_admin = cur.fetchone()

            if existing_admin:
                print("El usuario administrador ya existe.")
                return

            # Crear contraseña hasheada para el administrador
            admin_password_raw = 'admin_password_segura_123'  # ¡CAMBIA ESTO!
            hashed_admin_password = generate_password_hash(admin_password_raw, method='pbkdf2:sha256')

            # Insertar el usuario administrador
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
                        ('Administrador', admin_email, hashed_admin_password, 'administrador'))
            admin_id = cur.fetchone()[0]
            conn.commit()
            
            print("\n")
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
            if cur:
                cur.close()
            if conn:
                conn.close()

# Funciones para operaciones con el horario
def load_schedule(user_id):
    """Carga el horario para un usuario específico desde la base de datos."""
    conn = get_db_connection()
    schedule = {}
    if conn:
        cur = conn.cursor()
        try:
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

def save_schedule(day, time, subject, user_id):
    """Guarda o actualiza una materia en el horario para un usuario específico."""
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

def delete_schedule(day, time, user_id):
    """Elimina una materia del horario para un usuario específico."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM schedule WHERE day = %s AND time = %s AND user_id = %s", (day, time, user_id))
            conn.commit()
            print(f"Materia eliminada para {day} a las {time} del usuario {user_id}")
            return True
        except psycopg2.Error as e:
            print(f"Error al eliminar la materia: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# Funciones para operaciones con materias
def load_materias(user_id):
    """Carga las materias para un usuario específico desde la base de datos."""
    conn = get_db_connection()
    materias = []
    if conn:
        cur = conn.cursor()
        try:
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

def add_materia(name, user_id):
    """Agrega una nueva materia para un usuario."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO materias (name, user_id) VALUES (%s, %s) RETURNING id;", (name, user_id))
            materia_id = cur.fetchone()[0]
            conn.commit()
            print(f"Materia agregada: {name} con ID {materia_id} para usuario {user_id}")
            return materia_id
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            print(f"Error: La materia '{name}' ya existe.")
            return None
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al agregar la materia: {e}")
            return None
        finally:
            cur.close()
            conn.close()

def delete_materia(materia_id, user_id):
    """Elimina una materia por su ID, verificando que pertenezca al usuario."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM materias WHERE id = %s AND user_id = %s", (materia_id, user_id))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Materia eliminada con ID: {materia_id}")
                return True
            else:
                print(f"Error al eliminar materia: No se encontró materia con ID {materia_id}")
                return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar la materia: {e}")
            return False
        finally:
            cur.close()
            conn.close()

def get_materia_details(materia_id, user_id):
    """Carga los detalles de una materia por su ID, incluyendo tareas, exámenes y notas."""
    conn = get_db_connection()
    materia_details = None
    if conn:
        cur = conn.cursor()
        try:
            # Obtener el nombre de la materia
            cur.execute("SELECT id, name FROM materias WHERE id = %s AND user_id = %s", (materia_id, user_id))
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
                cur.execute("SELECT id, description, due_date, completed FROM tasks WHERE materia_id = %s AND user_id = %s ORDER BY due_date", (materia_id, user_id))
                tasks_rows = cur.fetchall()
                for task in tasks_rows:
                    materia_details['tasks'].append({'id': task[0], 'description': task[1], 'due_date': task[2], 'completed': task[3]})

                # Obtener los exámenes de la materia
                cur.execute("SELECT id, topic, exam_date, grade FROM exams WHERE materia_id = %s AND user_id = %s ORDER BY exam_date", (materia_id, user_id))
                exams_rows = cur.fetchall()
                for exam in exams_rows:
                    materia_details['exams'].append({'id': exam[0], 'topic': exam[1], 'exam_date': exam[2], 'grade': exam[3]})

                # Obtener las notas de la materia
                cur.execute("SELECT id, content FROM notes WHERE materia_id = %s AND user_id = %s", (materia_id, user_id))
                notes_rows = cur.fetchall()
                for note in notes_rows:
                    materia_details['notes'].append({'id': note[0], 'content': note[1]})

        except psycopg2.Error as e:
            print(f"Error al cargar detalles de la materia {materia_id}: {e}")
        finally:
            cur.close()
            conn.close()

    return materia_details

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
            if cur:
                cur.close()
            if conn:
                conn.close()

# Funciones para operaciones con tareas
def add_task(materia_id, description, due_date, user_id):
    """Agrega una nueva tarea para una materia."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO tasks (materia_id, description, due_date, user_id) VALUES (%s, %s, %s, %s) RETURNING id;", (materia_id, description, due_date, user_id))
            task_id = cur.fetchone()[0]
            conn.commit()
            print(f"Tarea agregada para materia {materia_id} con ID {task_id} para usuario {user_id}")
            return task_id
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al agregar la tarea: {e}")
            return None
        finally:
            cur.close()
            conn.close()

def delete_task(task_id, user_id):
    """Elimina una tarea por su ID, verificando que pertenezca al usuario."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, user_id))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Tarea eliminada con ID: {task_id}")
                return True
            else:
                print(f"Error al eliminar tarea: No se encontró tarea con ID {task_id}")
                return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar la tarea: {e}")
            return False
        finally:
            cur.close()
            conn.close()

def save_task(task_id, description, user_id):
    """Actualiza una tarea existente."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE tasks SET description = %s WHERE id = %s AND user_id = %s", (description, task_id, user_id))
            conn.commit()
            print(f"Tarea {task_id} actualizada.")
            return True
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al actualizar tarea {task_id}: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# Funciones para operaciones con exámenes
def add_exam(materia_id, topic, exam_date, grade, user_id):
    """Agrega un nuevo examen para una materia."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Validar fecha si se proporciona
            if exam_date:
                try:
                    exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
                except ValueError:
                    return None
            
            cur.execute("INSERT INTO exams (materia_id, topic, exam_date, grade, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;", (materia_id, topic, exam_date, grade, user_id))
            exam_id = cur.fetchone()[0]
            conn.commit()
            print(f"Examen agregado para materia {materia_id} con ID {exam_id} para usuario {user_id}")
            return exam_id
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al agregar el examen: {e}")
            return None
        finally:
            cur.close()
            conn.close()

def delete_exam(exam_id, user_id):
    """Elimina un examen por su ID, verificando que pertenezca al usuario."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM exams WHERE id = %s AND user_id = %s", (exam_id, user_id))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Examen eliminado con ID: {exam_id}")
                return True
            else:
                print(f"Error al eliminar examen: No se encontró examen con ID {exam_id}")
                return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar el examen: {e}")
            return False
        finally:
            cur.close()
            conn.close()

def save_exam(exam_id, topic, grade, exam_date, user_id):
    """Actualiza un examen existente."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Validar fecha si se proporciona
            if exam_date is not None:
                if exam_date == '':
                    exam_date = None
                else:
                    try:
                        exam_date = datetime.strptime(exam_date, '%Y-%m-%d').date()
                    except ValueError:
                        return False
            
            update_fields = []
            update_values = []
            
            if topic is not None:
                update_fields.append("topic = %s")
                update_values.append(topic)
            
            if 'grade' in locals():
                update_fields.append("grade = %s")
                update_values.append(grade)
            
            if exam_date is not None:
                update_fields.append("exam_date = %s")
                update_values.append(exam_date)
            
            if not update_fields:
                return False
            
            update_values.extend([exam_id, user_id])
            query = f"UPDATE exams SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
            
            cur.execute(query, update_values)
            conn.commit()
            print(f"Examen {exam_id} actualizado.")
            return True
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al actualizar examen {exam_id}: {e}")
            return False
        finally:
            cur.close()
            conn.close()

# Funciones para operaciones con notas
def add_note(materia_id, content, user_id):
    """Agrega una nueva nota para una materia."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO notes (materia_id, content, user_id) VALUES (%s, %s, %s) RETURNING id, created_at;", (materia_id, content, user_id))
            note_id, created_at = cur.fetchone()
            conn.commit()
            print(f"Nota agregada para materia {materia_id} con ID {note_id}")
            return note_id, created_at.strftime('%Y-%m-%d %H:%M:%S')
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al agregar la nota: {e}")
            return None, None
        finally:
            cur.close()
            conn.close()

def delete_note(note_id, user_id):
    """Elimina una nota por su ID, verificando que pertenezca al usuario."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, user_id))
            conn.commit()
            if cur.rowcount > 0:
                print(f"Nota eliminada con ID: {note_id}")
                return True
            else:
                print(f"Error al eliminar nota: No se encontró nota con ID {note_id}")
                return False
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al eliminar la nota: {e}")
            return False
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

def save_note(note_id, content, user_id):
    """Actualiza una nota existente."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE notes SET content = %s WHERE id = %s AND user_id = %s", (content, note_id, user_id))
            conn.commit()
            print(f"Nota {note_id} actualizada.")
            return True
        except psycopg2.Error as e:
            conn.rollback()
            print(f"Error al actualizar nota {note_id}: {e}")
            return False
        finally:
            cur.close()
            conn.close()
