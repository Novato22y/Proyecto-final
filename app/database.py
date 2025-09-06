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

## Eliminada la función create_tables, ahora la gestión de tablas es responsabilidad de SQLAlchemy

# =============================================================================
# FUNCIONES DEL HORARIO
# =============================================================================

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
    return False

# =============================================================================
# FUNCIONES DE MATERIAS
# =============================================================================

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
    return None

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
    return False

def get_materia_details(materia_id, user_id):
    """Carga los detalles de una materia por su ID, incluyendo tareas, exámenes y notas."""
    conn = get_db_connection()
    materia_details = None
    if conn:
        cur = conn.cursor()
        try:
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

                cur.execute("SELECT id, description, due_date, completed FROM tasks WHERE materia_id = %s AND user_id = %s ORDER BY due_date", (materia_id, user_id))
                tasks_rows = cur.fetchall()
                for task in tasks_rows:
                    materia_details['tasks'].append({'id': task[0], 'description': task[1], 'due_date': task[2], 'completed': task[3]})

                cur.execute("SELECT id, topic, exam_date, grade FROM exams WHERE materia_id = %s AND user_id = %s ORDER BY exam_date", (materia_id, user_id))
                exams_rows = cur.fetchall()
                for exam in exams_rows:
                    materia_details['exams'].append({'id': exam[0], 'topic': exam[1], 'exam_date': exam[2], 'grade': exam[3]})

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
    return False

# =============================================================================
# FUNCIONES DE TAREAS
# =============================================================================

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
    return None

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
    return False

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
    return False

# =============================================================================
# FUNCIONES DE EXÁMENES
# =============================================================================

def add_exam(materia_id, topic, exam_date, grade, user_id):
    """Agrega un nuevo examen para una materia."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
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
    return None

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
    return False

def save_exam(exam_id, topic, grade, exam_date, user_id):
    """Actualiza un examen existente."""
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
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
    return False

# =============================================================================
# FUNCIONES DE NOTAS
# =============================================================================

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
    return None, None

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
    return False

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
            if cur:
                cur.close()
            if conn:
                conn.close()
    return False
