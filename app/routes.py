# app/routes.py - Rutas y vistas de la aplicación
import os
import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
# Se elimina werkzeug.security porque los métodos ahora están en el modelo User
from app.database import (
    load_schedule, load_materias, save_schedule, 
    delete_schedule, add_materia, delete_materia, get_materia_details,
    add_task, delete_task, save_task, add_exam, delete_exam, save_exam,
    add_note, delete_note, save_note, is_materia_owned_by_user
)
from app.models import User
from . import db, oauth

# Imports para Google Calendar
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import google.oauth2.credentials

# Crear blueprints para organizar las rutas
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# =============================================================================
# RUTAS DE AUTENTICACIÓN (REFACTORIZADAS)
# =============================================================================

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Ruta para el registro de usuarios usando SQLAlchemy."""
    if current_user.is_authenticated:
        return redirect(url_for('main.principal'))

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            flash('Por favor, completa todos los campos.', 'warning')
            return render_template('register.html')

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
            return render_template('register.html')

        # Verificar si el usuario ya existe usando SQLAlchemy
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('El correo electrónico ya está registrado.', 'danger')
            return render_template('register.html')

        # Crear nuevo usuario con el modelo SQLAlchemy
        new_user = User(name=name, email=email)
        new_user.set_password(password) # Hashear y guardar contraseña
        
        db.session.add(new_user)
        db.session.commit()

        flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Ruta para el inicio de sesión usando SQLAlchemy."""
    if current_user.is_authenticated:
        return redirect(url_for('main.principal'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Por favor, ingresa correo y contraseña.', 'warning')
            return render_template('sesion.html')

        # Buscar usuario con SQLAlchemy
        user = User.query.filter_by(email=email).first()

        # Verificar usuario y contraseña con los métodos del modelo
        if user and user.check_password(password):
            login_user(user, remember=True) # remember=True es una buena práctica
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.principal'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'danger')

    return render_template('sesion.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Ruta para cerrar sesión"""
    logout_user()
    if 'google_credentials' in session:
        session.pop('google_credentials')
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('main.principal'))

# --- Rutas para Google Sign-In ---

@auth_bp.route('/google/login')
def google_login_auth():
    """
    Redirige al usuario a la página de consentimiento de Google para el Sign-In.
    """
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_bp.route('/google/callback')
def google_callback():
    """
    Ruta de callback que Google invoca tras la autorización del usuario para el Sign-In.
    """
    try:
        token = oauth.google.authorize_access_token()
        user_info = oauth.google.userinfo()
    except Exception as e:
        flash('Ocurrió un error durante la autenticación con Google. Por favor, inténtalo de nuevo.', 'danger')
        current_app.logger.error(f"Error en callback de Google Sign-In: {e}")
        return redirect(url_for('auth.login'))

    google_id = user_info.get('sub')
    email = user_info.get('email')
    name = user_info.get('name')

    if not email:
        flash('No se pudo obtener el email de tu cuenta de Google. Asegúrate de dar los permisos necesarios.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()

    if user:
        if not user.google_id:
            user.google_id = google_id
            db.session.commit()
    else:
        user = User(
            google_id=google_id,
            email=email,
            name=name,
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    flash(f'¡Bienvenido, {user.name}!', 'success')
    
    return redirect(url_for('main.principal'))


# =============================================================================
# RUTAS DE INTEGRACIÓN CON GOOGLE CALENDAR (EXISTENTES)
# =============================================================================

def get_google_flow():
    """Helper para crear un objeto Flow de Google OAuth para Calendar."""
    redirect_uri = url_for('main.callback', _external=True)
    if not current_app.debug and redirect_uri.startswith('http://'):
        redirect_uri = redirect_uri.replace('http://', 'https://', 1)

    return Flow.from_client_config(
        client_config={
            "web": {
                "client_id": current_app.config['GOOGLE_CLIENT_ID'],
                "client_secret": current_app.config['GOOGLE_CLIENT_SECRET'],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "redirect_uris": [redirect_uri],
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar.events.readonly'],
        redirect_uri=redirect_uri
    )

@main_bp.route('/google-login')
@login_required
def google_login():
    """Inicia el flujo de OAuth para conectar con Google Calendar."""
    flow = get_google_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@main_bp.route('/callback')
@login_required
def callback():
    """Maneja el callback de OAuth 2.0 de Google para Calendar."""
    try:
        state = session.pop('state', None)
        flow = get_google_flow()
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials
        session['google_credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        flash('Tu cuenta de Google ha sido conectada exitosamente.', 'success')
    except Exception as e:
        flash(f"Error durante la autenticación con Google: {e}", "error")
        
    return redirect(url_for('main.principal'))

@main_bp.route('/google-logout')
@login_required
def google_logout():
    """Limpia las credenciales de Google de la sesión."""
    if 'google_credentials' in session:
        session.pop('google_credentials')
        flash('Has desconectado tu cuenta de Google.', 'success')
    return redirect(url_for('main.principal'))

# =============================================================================
# RUTAS PRINCIPALES
# =============================================================================

@main_bp.route('/')
def principal():
    """Página principal de la aplicación"""
    schedule = {}
    materias = []
    calendar_events = []

    if current_user.is_authenticated:
        schedule = load_schedule(current_user.id)
        materias = load_materias(current_user.id)

        if 'google_credentials' in session:
            try:
                creds = google.oauth2.credentials.Credentials(**session['google_credentials'])
                
                if creds.expired and creds.refresh_token:
                    from google.auth.transport.requests import Request
                    creds.refresh(Request())
                    session['google_credentials'] = {
                        'token': creds.token, 'refresh_token': creds.refresh_token,
                        'token_uri': creds.token_uri, 'client_id': creds.client_id,
                        'client_secret': creds.client_secret, 'scopes': creds.scopes
                    }

                service = build('calendar', 'v3', credentials=creds)
                now = datetime.datetime.utcnow().isoformat() + 'Z'
                events_result = service.events().list(
                    calendarId='primary', timeMin=now,
                    maxResults=10, singleEvents=True,
                    orderBy='startTime'
                ).execute()
                calendar_events = events_result.get('items', [])

            except Exception as e:
                flash(f"Error al obtener eventos de Google Calendar: {e}. Por favor, intenta reconectar tu cuenta.", "error")
                session.pop('google_credentials', None)

    return render_template("index.html", schedule=schedule, materias=materias, current_user=current_user, calendar_events=calendar_events)


@main_bp.route('/profile')
@login_required
def profile():
    """Muestra la página de perfil del usuario."""
    return render_template('profile.html', user=current_user)


# ... (resto de las rutas sin cambios) ...
# =============================================================================
# RUTAS DEL HORARIO
# =============================================================================

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

# =============================================================================
# RUTAS DE MATERIAS
# =============================================================================

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

# =============================================================================
# RUTAS DE TAREAS, EXÁMENES Y NOTAS (sin cambios)
# =============================================================================
@main_bp.route('/add_task', methods=['POST'])
@login_required
def add_task_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    description = data.get('description')
    due_date = data.get('due_date')
    if not is_materia_owned_by_user(materia_id, current_user.id):
        return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
    task_id = add_task(materia_id, description, due_date, current_user.id)
    return jsonify({'status': 'success', 'task_id': task_id}) if task_id else jsonify({'status': 'error'}), 500

@main_bp.route('/delete_task', methods=['POST'])
@login_required
def delete_task_route():
    task_id = request.get_json().get('task_id')
    if delete_task(task_id, current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404

@main_bp.route('/save_task', methods=['POST'])
@login_required
def save_task_route():
    data = request.get_json()
    task_id = data.get('task_id')
    description = data.get('description')
    if save_task(task_id, description, current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@main_bp.route('/add_exam', methods=['POST'])
@login_required
def add_exam_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    if not is_materia_owned_by_user(materia_id, current_user.id):
        return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
    exam_id = add_exam(materia_id, data.get('topic'), data.get('exam_date'), data.get('grade'), current_user.id)
    return jsonify({'status': 'success', 'exam_id': exam_id}) if exam_id else jsonify({'status': 'error'}), 500

@main_bp.route('/delete_exam', methods=['POST'])
@login_required
def delete_exam_route():
    exam_id = request.get_json().get('exam_id')
    if delete_exam(exam_id, current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404

@main_bp.route('/save_exam', methods=['POST'])
@login_required
def save_exam_route():
    data = request.get_json()
    exam_id = data.get('exam_id')
    if save_exam(exam_id, data.get('topic'), data.get('grade'), data.get('exam_date'), current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@main_bp.route('/add_note', methods=['POST'])
@login_required
def add_note_route():
    data = request.get_json()
    materia_id = data.get('materia_id')
    if not is_materia_owned_by_user(materia_id, current_user.id):
        return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
    note_id, created_at = add_note(materia_id, data.get('content'), current_user.id)
    return jsonify({'status': 'success', 'note_id': note_id, 'created_at': created_at}) if note_id else jsonify({'status': 'error'}), 500

@main_bp.route('/delete_note', methods=['POST'])
@login_required
def delete_note_route():
    note_id = request.get_json().get('note_id')
    if delete_note(note_id, current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404

@main_bp.route('/save_note', methods=['POST'])
@login_required
def save_note_route():
    data = request.get_json()
    note_id = data.get('note_id')
    if save_note(note_id, data.get('content'), current_user.id):
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

# =============================================================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# =============================================================================

