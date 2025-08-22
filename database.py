# database.py - Funciones de base de datos
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

def get_db_connection():
    """Establece una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
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
                    id SERIAL PRIMARY KEY,
                    day VARCHAR(20) NOT NULL,
                    time VARCHAR(10) NOT NULL,
                    subject VARCHAR(100),
                    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                    UNIQUE(day, time, user_id)
                )
            """)
            print("Tabla 'schedule' verificada/creada.")

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

def save_schedule(day, time, subject, user_id):
    """Guarda o actualiza una materia en el horario para un usuario específico en la base de datos."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("UPDATE schedule SET subject = %s WHERE day = %s AND time = %s AND user_id = %s", (subject, day, time, user_id))
            if cur.rowcount == 0:
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

                cur.execute("SELECT id, description, due_date, completed FROM tasks WHERE materia_id = %s ORDER BY due_date", (materia_id,))
                tasks_rows = cur.fetchall()
                for task in tasks_rows:
                    materia_details['tasks'].append({'id': task[0], 'description': task[1], 'due_date': task[2], 'completed': task[3]})

                cur.execute("SELECT id, topic, exam_date, grade FROM exams WHERE materia_id = %s ORDER BY exam_date", (materia_id,))
                exams_rows = cur.fetchall()
                for exam in exams_rows:
                    materia_details['exams'].append({'id': exam[0], 'topic': exam[1], 'exam_date': exam[2], 'grade': exam[3]})

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
