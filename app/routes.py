# app/routes.py - Rutas y vistas de la aplicación
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import (
    create_tables, create_admin_user, load_schedule, load_materias, save_schedule, 
    delete_schedule, add_materia, delete_materia, get_materia_details,
    add_task, delete_task, save_task, add_exam, delete_exam, save_exam,
    add_note, delete_note, save_note, is_materia_owned_by_user,
    user_exists, create_user
)
from app.models import User

# Crear blueprints para organizar las rutas
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# ===== RUTAS DE AUTENTICACIÓN =====

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('main.principal'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validaciones básicas
        if not name or not email or not password:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
            return render_template('register.html')

        # Crear el usuario usando la nueva función
        user_id, error_message = create_user(name, email, password)
        
        if user_id:
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(error_message, 'danger')
            return render_template('register.html')

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para el inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('main.principal'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor, ingresa correo y contraseña.', 'warning')
            return render_template('sesion.html')

        from app.database import get_db_connection
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
                user_data = cur.fetchone()

                if user_data and check_password_hash(user_data[3], password):
                    user = User(id=user_data[0], name=user_data[1], email=user_data[2], role=user_data[4])
                    login_user(user)
                    print(f"Usuario logeado: {user.name} ({user.email}) con rol {user.role}")
                    # Redirigir a la página principal o a la página solicitada
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('main.principal'))
                else:
                    flash('Correo electrónico o contraseña incorrectos.', 'danger')
            except Exception as e:
                print(f"Error al intentar login: {e}")
                flash('Ocurrió un error al intentar iniciar sesión.', 'danger')
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()

    return render_template('sesion.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión"""
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('main.principal'))

# ===== RUTAS PRINCIPALES =====

@main_bp.route('/')
def principal():
    """Página principal de la aplicación"""
    create_tables()  # Asegúrate de que las tablas existan

    schedule = {}
    materias = []

    if current_user.is_authenticated:
        # Cargar datos solo para el usuario logeado
        schedule = load_schedule(current_user.id)
        materias = load_materias(current_user.id)

    # Pasar current_user a la plantilla para mostrar el nombre o el enlace de login/registro
    return render_template("index.html", schedule=schedule, materias=materias, current_user=current_user)

# ===== RUTAS DEL HORARIO =====

@main_bp.route('/save_schedule', methods=['POST'])
@login_required
def save_schedule_route():
    """Ruta para guardar el horario"""
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')
    if day and time and subject is not None:
        save_schedule(day, time, subject, current_user.id)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

@main_bp.route('/add_schedule', methods=['POST'])
@login_required
def add_schedule_route():
    """Ruta para agregar una materia al horario"""
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    subject = data.get('subject')

    if day and time and subject and current_user.is_authenticated:
        save_schedule(day, time, subject, current_user.id)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400

@main_bp.route('/delete_schedule', methods=['POST'])
@login_required
def delete_schedule_route():
    """Ruta para eliminar una materia del horario"""
    data = request.get_json()
    day = data.get('day')
    time = data.get('time')
    if day and time:
        if delete_schedule(day, time, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Error al eliminar la materia'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400

# ===== RUTAS DE MATERIAS =====

@main_bp.route('/add_materia', methods=['POST'])
@login_required
def add_materia_route():
    """Ruta para agregar una nueva materia"""
    data = request.get_json()
    materia_name = data.get('name')

    if materia_name and current_user.is_authenticated:
        materia_id = add_materia(materia_name, current_user.id)
        if materia_id:
            return jsonify({'status': 'success', 'materia_id': materia_id})
        else:
            return jsonify({'status': 'error', 'message': 'La materia ya existe.'}), 400
    else:
        return jsonify({'status': 'error', 'message': 'Nombre de materia no proporcionado'}), 400

@main_bp.route('/delete_materia', methods=['POST'])
@login_required
def delete_materia_route():
    """Ruta para eliminar una materia"""
    data = request.get_json()
    materia_id = data.get('materia_id')

    if materia_id is not None:
        if delete_materia(materia_id, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Materia no encontrada'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'ID de materia no proporcionado'}), 400

@main_bp.route('/materia/<int:materia_id>')
@login_required
def materia_detalle(materia_id):
    """Ruta para mostrar los detalles de una materia"""
    materia_details = get_materia_details(materia_id, current_user.id)
    if materia_details:
        return render_template('subject_detail.html', materia=materia_details)
    else:
        return "Materia no encontrada", 404

# ===== RUTAS DE TAREAS =====

@main_bp.route('/add_task', methods=['POST'])
@login_required
def add_task_route():
    """Ruta para agregar una nueva tarea"""
    data = request.get_json()
    materia_id = data.get('materia_id')
    description = data.get('description')
    due_date = data.get('due_date')

    if materia_id is not None and description and current_user.is_authenticated:
        if not is_materia_owned_by_user(materia_id, current_user.id):
            return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

        task_id = add_task(materia_id, description, due_date, current_user.id)
        if task_id:
            return jsonify({'status': 'success', 'task_id': task_id})
        else:
            return jsonify({'status': 'error', 'message': 'Error al agregar la tarea'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para la tarea'}), 400

@main_bp.route('/delete_task', methods=['POST'])
@login_required
def delete_task_route():
    """Ruta para eliminar una tarea"""
    data = request.get_json()
    task_id = data.get('task_id')

    if task_id is not None and current_user.is_authenticated:
        if delete_task(task_id, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Tarea no encontrada'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'ID de tarea no proporcionado'}), 400

@main_bp.route('/save_task', methods=['POST'])
@login_required
def save_task_route():
    """Ruta para actualizar una tarea"""
    data = request.get_json()
    task_id = data.get('task_id')
    description = data.get('description')

    if task_id is not None and description is not None and current_user.is_authenticated:
        if save_task(task_id, description, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Error al actualizar tarea'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para actualizar tarea'}), 400

# ===== RUTAS DE EXÁMENES =====

@main_bp.route('/add_exam', methods=['POST'])
@login_required
def add_exam_route():
    """Ruta para agregar un nuevo examen"""
    data = request.get_json()
    materia_id = data.get('materia_id')
    topic = data.get('topic')
    exam_date_str = data.get('exam_date')
    grade = data.get('grade')

    if materia_id is None or not topic or not current_user.is_authenticated:
        return jsonify({'status': 'error', 'message': 'Datos incompletos o usuario no autenticado'}), 400

    if not is_materia_owned_by_user(materia_id, current_user.id):
        return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

    exam_id = add_exam(materia_id, topic, exam_date_str, grade, current_user.id)
    if exam_id:
        return jsonify({'status': 'success', 'exam_id': exam_id})
    else:
        return jsonify({'status': 'error', 'message': 'Error al agregar el examen'}), 500

@main_bp.route('/delete_exam', methods=['POST'])
@login_required
def delete_exam_route():
    """Ruta para eliminar un examen"""
    data = request.get_json()
    exam_id = data.get('exam_id')

    if exam_id is not None and current_user.is_authenticated:
        if delete_exam(exam_id, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Examen no encontrado'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado'}), 400

@main_bp.route('/save_exam', methods=['POST'])
@login_required
def save_exam_route():
    """Ruta para actualizar un examen"""
    data = request.get_json()
    exam_id = data.get('exam_id')
    topic = data.get('topic')
    grade = data.get('grade')
    exam_date_str = data.get('exam_date')

    if exam_id is None or not current_user.is_authenticated:
        return jsonify({'status': 'error', 'message': 'ID de examen no proporcionado o usuario no autenticado'}), 400

    if save_exam(exam_id, topic, grade, exam_date_str, current_user.id):
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Error al actualizar examen'}), 500

# ===== RUTAS DE NOTAS =====

@main_bp.route('/add_note', methods=['POST'])
@login_required
def add_note_route():
    """Ruta para agregar una nueva nota"""
    data = request.get_json()
    materia_id = data.get('materia_id')
    content = data.get('content')

    if materia_id is not None and content and current_user.is_authenticated:
        if not is_materia_owned_by_user(materia_id, current_user.id):
            return jsonify({'status': 'error', 'message': 'Materia no encontrada o no pertenece al usuario'}), 403

        note_id, created_at = add_note(materia_id, content, current_user.id)
        if note_id:
            return jsonify({'status': 'success', 'note_id': note_id, 'created_at': created_at})
        else:
            return jsonify({'status': 'error', 'message': 'Error al agregar la nota'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para la nota'}), 400

@main_bp.route('/delete_note', methods=['POST'])
@login_required
def delete_note_route():
    """Ruta para eliminar una nota"""
    data = request.get_json()
    note_id = data.get('note_id')

    if note_id is not None and current_user.is_authenticated:
        if delete_note(note_id, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Nota no encontrada'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'ID de nota no proporcionado'}), 400

@main_bp.route('/save_note', methods=['POST'])
@login_required
def save_note_route():
    """Ruta para actualizar una nota"""
    data = request.get_json()
    note_id = data.get('note_id')
    content = data.get('content')

    if note_id is not None and content is not None and current_user.is_authenticated:
        if save_note(note_id, content, current_user.id):
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error', 'message': 'Error al actualizar nota'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'Datos incompletos para actualizar nota'}), 400

# ===== INICIALIZACIÓN DE LA BASE DE DATOS =====

def init_db():
    """Inicializa la base de datos creando las tablas y el usuario administrador"""
    create_tables()
    create_admin_user()

# Ejecutar la inicialización cuando se importe el módulo
init_db()
