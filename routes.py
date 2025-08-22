# routes.py - Todas las rutas de la aplicación
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import database
from models import User

def init_routes(app):
    """Inicializa todas las rutas de la aplicación"""
    
    @app.route('/')
    def principal():
        """Ruta principal de la aplicación"""
        database.create_table()
        
        schedule = {}
        materias = []
        
        if current_user.is_authenticated:
            schedule = database.load_schedule(current_user.id)
            materias = database.load_materias(current_user.id)
        
        return render_template("index.html", schedule=schedule, materias=materias, current_user=current_user)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Ruta para registro de usuarios"""
        if current_user.is_authenticated:
            return redirect(url_for('principal'))

        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = 'cliente'

            if not name or not email or not password:
                flash('Por favor, completa todos los campos.', 'warning')
                return render_template('register.html')

            if User.user_exists(email):
                flash('El correo electrónico ya está registrado.', 'danger')
                return render_template('register.html')

            user = User.create_user(name, email, password, role)
            if user:
                flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ocurrió un error durante el registro.', 'danger')

        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Ruta para inicio de sesión"""
        if current_user.is_authenticated:
            return redirect(url_for('principal'))

        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            if not email or not password:
                flash('Por favor, ingresa correo y contraseña.', 'warning')
                return render_template('login.html')

            user = User.authenticate_user(email, password)
            if user:
                login_user(user)
                print(f"Usuario logeado: {user.name} ({user.email}) con rol {user.role}")
                next_page = request.args.get('next')
                return redirect(next_page or url_for('principal'))
            else:
                flash('Correo electrónico o contraseña incorrectos.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    @login_required
    def logout():
        """Ruta para cerrar sesión"""
        logout_user()
        flash('Has cerrado sesión exitosamente.', 'success')
        return redirect(url_for('principal'))

    # Rutas para el horario
    @app.route('/save_schedule', methods=['POST'])
    @login_required
    def save_schedule_route():
        """Guarda o actualiza el horario"""
        data = request.get_json()
        day = data.get('day')
        time = data.get('time')
        subject = data.get('subject')
        
        if day and time and subject is not None:
            database.save_schedule(day, time, subject, current_user.id)
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

    @app.route('/add_schedule', methods=['POST'])
    @login_required
    def add_schedule_route():
        """Agrega una nueva materia al horario"""
        data = request.get_json()
        day = data.get('day')
        time = data.get('time')
        subject = data.get('subject')

        if day and time and subject and current_user.is_authenticated:
            database.save_schedule(day, time, subject, current_user.id)
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400

    @app.route('/delete_schedule', methods=['POST'])
    @login_required
    def delete_schedule_route():
        """Elimina una materia del horario"""
        data = request.get_json()
        day = data.get('day')
        time = data.get('time')
        
        if day and time:
            if database.delete_schedule(day, time):
                return jsonify({'status': 'success'})
            else:
                return jsonify({'status': 'error', 'message': 'Error al eliminar la materia'}), 500
        else:
            return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

    # Rutas para materias
    @app.route('/add_materia', methods=['POST'])
    @login_required
    def add_materia_route():
        """Agrega una nueva materia"""
        data = request.get_json()
        materia_name = data.get('name')

        if materia_name and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO materias (name, user_id) VALUES (%s, %s) RETURNING id;", 
                               (materia_name, current_user.id))
                    materia_id = cur.fetchone()[0]
                    conn.commit()
                    print(f"Materia agregada: {materia_name} con ID {materia_id} para usuario {current_user.id}")
                    return jsonify({'status': 'success', 'materia_id': materia_id})
                except Exception as e:
                    conn.rollback()
                    print(f"Error al agregar la materia: {e}")
                    return jsonify({'status': 'error', 'message': 'Error al agregar la materia'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'Nombre de materia no proporcionado'}), 400

    @app.route('/delete_materia', methods=['POST'])
    @login_required
    def delete_materia_route():
        """Elimina una materia"""
        data = request.get_json()
        materia_id = data.get('materia_id')

        if materia_id is not None:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM materias WHERE id = %s AND user_id = %s", (materia_id, current_user.id))
                    conn.commit()
                    if cur.rowcount > 0:
                        print(f"Materia eliminada con ID: {materia_id}")
                        return jsonify({'status': 'success'})
                    else:
                        print(f"Error al eliminar materia: No se encontró materia con ID {materia_id}")
                        return jsonify({'status': 'error', 'message': 'Materia no encontrada'}), 404
                except Exception as e:
                    conn.rollback()
                    print(f"Error al eliminar la materia: {e}")
                    return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar la materia'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'ID de materia no proporcionado'}), 400

    @app.route('/materia/<int:materia_id>')
    def materia_detalle(materia_id):
        """Muestra los detalles de una materia específica"""
        materia_details = database.get_materia_details(materia_id)
        if materia_details:
            return render_template('subject_detail.html', materia=materia_details)
        else:
            return "Materia no encontrada", 404

    # Rutas para tareas, exámenes y notas
    @app.route('/add_task', methods=['POST'])
    @login_required
    def add_task_route():
        """Agrega una nueva tarea"""
        data = request.get_json()
        materia_id = data.get('materia_id')
        description = data.get('description')
        due_date = data.get('due_date')

        if materia_id is not None and description and current_user.is_authenticated:
            if not database.is_materia_owned_by_user(materia_id, current_user.id):
                return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO tasks (materia_id, description, due_date, user_id) VALUES (%s, %s, %s, %s) RETURNING id;", 
                               (materia_id, description, due_date, current_user.id))
                    task_id = cur.fetchone()[0]
                    conn.commit()
                    print(f"Tarea agregada para materia {materia_id} con ID {task_id} para usuario {current_user.id}")
                    return jsonify({'status': 'success', 'task_id': task_id})
                except Exception as e:
                    conn.rollback()
                    print(f"Error al agregar la tarea: {e}")
                    return jsonify({'status': 'error', 'message': 'Error al agregar la tarea'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'Datos incompletos para la tarea'}), 400

    @app.route('/add_exam', methods=['POST'])
    @login_required
    def add_exam_route():
        """Agrega un nuevo examen"""
        data = request.get_json()
        materia_id = data.get('materia_id')
        topic = data.get('topic')
        exam_date_str = data.get('exam_date')
        grade = data.get('grade')

        if materia_id is None or not topic or not current_user.is_authenticated:
            return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400

        if not database.is_materia_owned_by_user(materia_id, current_user.id):
            return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

        exam_date = None
        if exam_date_str:
            try:
                exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'status': 'error', 'message': 'Formato de fecha de examen inválido. Use YYYY-MM-DD.'}), 400

        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO exams (materia_id, topic, exam_date, grade, user_id) VALUES (%s, %s, %s, %s, %s) RETURNING id;", 
                           (materia_id, topic, exam_date, grade, current_user.id))
                exam_id = cur.fetchone()[0]
                conn.commit()
                print(f"Examen agregado para materia {materia_id} con ID {exam_id} para usuario {current_user.id}")
                return jsonify({'status': 'success', 'exam_id': exam_id})
            except Exception as e:
                conn.rollback()
                print(f"Error al agregar el examen: {e}")
                return jsonify({'status': 'error', 'message': 'Error al agregar el examen'}), 500
            finally:
                cur.close()
                conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'Error al conectar a la base de datos'}), 500

    @app.route('/add_note', methods=['POST'])
    @login_required
    def add_note_route():
        """Agrega una nueva nota"""
        data = request.get_json()
        materia_id = data.get('materia_id')
        content = data.get('content')

        if materia_id is not None and content and current_user.is_authenticated:
            if not database.is_materia_owned_by_user(materia_id, current_user.id):
                return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    print(f"Intentando agregar nota para materia_id: {materia_id}, contenido: {content[:50]}... para usuario {current_user.id}")
                    cur.execute("INSERT INTO notes (materia_id, content, user_id) VALUES (%s, %s, %s) RETURNING id, created_at;", 
                               (materia_id, content, current_user.id))
                    note_id, created_at = cur.fetchone()
                    conn.commit()
                    print(f"Nota agregada para materia {materia_id} con ID {note_id}")
                    return jsonify({'status': 'success', 'note_id': note_id, 'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')})
                except Exception as e:
                    conn.rollback()
                    print(f"Error al agregar la nota: {e}")
                    return jsonify({'status': 'error', 'message': 'Error al agregar la nota'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'Datos incompletos para la nota'}), 400

    # Rutas para eliminar elementos
    @app.route('/delete_task', methods=['POST'])
    @login_required
    def delete_task_route():
        """Elimina una tarea"""
        data = request.get_json()
        task_id = data.get('task_id')

        if task_id is not None and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM tasks WHERE id = %s AND user_id = %s", (task_id, current_user.id))
                    conn.commit()
                    if cur.rowcount > 0:
                        print(f"Tarea eliminada con ID: {task_id}")
                        return jsonify({'status': 'success'})
                    else:
                        print(f"Error al eliminar tarea: No se encontró tarea con ID {task_id}")
                        return jsonify({'status': 'error', 'message': 'Tarea no encontrada'}), 404
                except Exception as e:
                    conn.rollback()
                    print(f"Error al eliminar la tarea: {e}")
                    return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar la tarea'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'ID de tarea no proporcionado'}), 400

    @app.route('/delete_exam', methods=['POST'])
    @login_required
    def delete_exam_route():
        """Elimina un examen"""
        data = request.get_json()
        exam_id = data.get('exam_id')

        if exam_id is not None and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM exams WHERE id = %s AND user_id = %s", (exam_id, current_user.id))
                    conn.commit()
                    if cur.rowcount > 0:
                        print(f"Examen eliminado con ID: {exam_id}")
                        return jsonify({'status': 'success'})
                    else:
                        print(f"Error al eliminar examen: No se encontró examen con ID {exam_id}")
                        return jsonify({'status': 'error', 'message': 'Examen no encontrado'}), 404
                except Exception as e:
                    conn.rollback()
                    print(f"Error al eliminar el examen: {e}")
                    return jsonify({'status': 'error', 'message': 'Error en la base de datos al eliminar el examen'}), 500
                finally:
                    cur.close()
                    conn.close()
        else:
            return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado'}), 400

    @app.route('/delete_note', methods=['POST'])
    @login_required
    def delete_note_route():
        """Elimina una nota"""
        data = request.get_json()
        note_id = data.get('note_id')

        if note_id is not None and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM notes WHERE id = %s AND user_id = %s", (note_id, current_user.id))
                    conn.commit()
                    if cur.rowcount > 0:
                        print(f"Nota eliminada con ID: {note_id}")
                        return jsonify({'status': 'success'})
                    else:
                        print(f"Error al eliminar nota: No se encontró nota con ID {note_id}")
                        return jsonify({'status': 'error', 'message': 'Nota no encontrada'}), 404
                except Exception as e:
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

    # Rutas para guardar/actualizar elementos
    @app.route('/save_task', methods=['POST'])
    @login_required
    def save_task_route():
        """Guarda/actualiza una tarea"""
        data = request.get_json()
        task_id = data.get('task_id')
        description = data.get('description')

        if task_id is not None and description is not None and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE tasks SET description = %s WHERE id = %s AND user_id = %s", 
                               (description, task_id, current_user.id))
                    conn.commit()
                    print(f"Tarea {task_id} actualizada.")
                    return jsonify({'status': 'success'})
                except Exception as e:
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
    @login_required
    def save_exam_route():
        """Guarda/actualiza un examen"""
        data = request.get_json()
        exam_id = data.get('exam_id')
        topic = data.get('topic')
        grade = data.get('grade')
        exam_date_str = data.get('exam_date')

        if exam_id is None or not current_user.is_authenticated:
            return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado o usuario no autenticado'}), 400

        exam_date = None
        if exam_date_str is not None:
            if exam_date_str == '':
                exam_date = None
            else:
                try:
                    exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'status': 'error', 'message': 'Formato de fecha de examen inválido. Use YYYY-MM-DD.'}), 400

        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                update_fields = []
                update_values = []
                if topic is not None:
                    update_fields.append("topic = %s")
                    update_values.append(topic)

                if 'grade' in data:
                    update_fields.append("grade = %s")
                    update_values.append(grade)

                if exam_date_str is not None:
                    update_fields.append("exam_date = %s")
                    update_values.append(exam_date)

                if not update_fields:
                    return jsonify({'status': 'error', 'message': 'No hay campos para actualizar'}), 400

                update_values.append(exam_id)
                update_values.append(current_user.id)

                query = f"UPDATE exams SET {', '.join(update_fields)} WHERE id = %s AND user_id = %s"
                cur.execute(query, update_values)
                conn.commit()
                print(f"Examen {exam_id} actualizado.")
                return jsonify({'status': 'success'})
            except Exception as e:
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
    @login_required
    def save_note_route():
        """Guarda/actualiza una nota"""
        data = request.get_json()
        note_id = data.get('note_id')
        content = data.get('content')

        if note_id is not None and content is not None and current_user.is_authenticated:
            conn = database.get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE notes SET content = %s WHERE id = %s AND user_id = %s", 
                               (content, note_id, current_user.id))
                    conn.commit()
                    print(f"Nota {note_id} actualizada.")
                    return jsonify({'status': 'success'})
                except Exception as e:
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
