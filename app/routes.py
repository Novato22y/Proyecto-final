
# app/routes.py - Rutas y vistas de la aplicación
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User
from . import db, oauth


main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
# =============================
# API de Recordatorios (Calendario)
@main_bp.route('/api/recordatorios/<int:id>', methods=['PUT'])
@login_required
def actualizar_recordatorio(id):
    recordatorio = Recordatorio.query.filter_by(id=id, usuario_id=current_user.id).first()
    if not recordatorio:
        return jsonify({'error': 'No encontrado'}), 404
    data = request.get_json()
    recordatorio.fecha = data.get('fecha', recordatorio.fecha)
    recordatorio.titulo = data.get('titulo', recordatorio.titulo)
    recordatorio.descripcion = data.get('descripcion', recordatorio.descripcion)
    recordatorio.importancia = data.get('importancia', recordatorio.importancia)
    db.session.commit()
    return jsonify({'success': True})
# =============================
from flask import jsonify
from app.models import Recordatorio

@main_bp.route('/api/recordatorios/<fecha>', methods=['GET'])
@login_required
def get_recordatorios(fecha):
    recordatorios = Recordatorio.query.filter_by(fecha=fecha, usuario_id=current_user.id).all()
    resultado = [
        {
            'id': r.id,
            'fecha': r.fecha,
            'titulo': r.titulo,
            'descripcion': r.descripcion,
            'importancia': r.importancia
        } for r in recordatorios
    ]
    return jsonify(resultado)

@main_bp.route('/api/recordatorios', methods=['POST'])
@login_required
def crear_recordatorio():
    data = request.get_json()
    nuevo = Recordatorio(
        usuario_id=current_user.id,
        fecha=data.get('fecha'),
        titulo=data.get('titulo'),
        descripcion=data.get('descripcion'),
        importancia=data.get('importancia', 'baja')
    )
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({'success': True, 'id': nuevo.id}), 201

@main_bp.route('/api/recordatorios/<int:id>', methods=['DELETE'])
@login_required
def eliminar_recordatorio(id):
    recordatorio = Recordatorio.query.filter_by(id=id, usuario_id=current_user.id).first()
    if not recordatorio:
        return jsonify({'error': 'No encontrado'}), 404
    db.session.delete(recordatorio)
    db.session.commit()
    return jsonify({'success': True})

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
    scopes = [
        'openid',
        'email',
        'profile'
    ]
    print("Redirect URI para Google OAuth:", redirect_uri)
    return oauth.google.authorize_redirect(redirect_uri, scope=" ".join(scopes))


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
# RUTAS PRINCIPALES
# =============================================================================
@main_bp.route('/base')
def ver_base():
    return render_template('base.html')
@main_bp.route('/')
def principal():
    """Página principal de la aplicación"""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.register'))
    return render_template("principal.html", current_user=current_user)

@main_bp.route('/profile')
@login_required
def profile():
    """Muestra la página de perfil del usuario."""
    return render_template('profile.html', user=current_user)

@main_bp.route('/prueba')
def ver_prueba():
    return render_template('prueba.html')
@main_bp.route('/calendario')
def ver_calendario():
    return render_template('calendario.html')

@main_bp.route('/upload_profile_photo', methods=['POST'])
@login_required
def upload_profile_photo():
    import uuid
    from werkzeug.utils import secure_filename
    foto = request.files.get('foto')
    if not foto:
        flash('No se seleccionó ninguna imagen.', 'warning')
        return redirect(url_for('main.profile'))
    ext = foto.filename.rsplit('.', 1)[-1].lower()
    if ext not in ['jpg', 'jpeg', 'png', 'gif']:
        flash('Formato de imagen no permitido.', 'danger')
        return redirect(url_for('main.profile'))
    filename = f"{current_user.id}_{uuid.uuid4().hex}.{ext}"
    path = os.path.join(current_app.static_folder, 'images', 'profiles')
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, filename)
    foto.save(file_path)
    # Actualizar usuario (requiere campo en modelo)
    current_user.profile_image = f"images/profiles/{filename}"
    db.session.commit()
    flash('Foto de perfil actualizada.', 'success')
    return redirect(url_for('main.profile'))
@main_bp.route('/update_password', methods=['POST'])
@login_required
def update_password():
    nueva_contrasena = request.form.get('nueva_contrasena')
    confirmar_contrasena = request.form.get('confirmar_contrasena')
    if not nueva_contrasena or not confirmar_contrasena:
        flash('Debes completar ambos campos de contraseña.', 'warning')
        return redirect(url_for('main.profile'))
    if nueva_contrasena != confirmar_contrasena:
        flash('Las contraseñas no coinciden.', 'danger')
        return redirect(url_for('main.profile'))
    if len(nueva_contrasena) < 6:
        flash('La contraseña debe tener al menos 6 caracteres.', 'warning')
        return redirect(url_for('main.profile'))
    current_user.set_password(nueva_contrasena)
    db.session.commit()
    flash('Contraseña actualizada correctamente.', 'success')
    return redirect(url_for('main.profile'))

@main_bp.route('/update_name', methods=['POST'])
@login_required
def update_name():
    nuevo_nombre = request.form.get('nuevo_nombre')
    if not nuevo_nombre or len(nuevo_nombre) < 2:
        flash('El nombre debe tener al menos 2 caracteres.', 'warning')
        return redirect(url_for('main.profile'))
    current_user.name = nuevo_nombre
    db.session.commit()
    flash('Nombre actualizado correctamente.', 'success')
    return redirect(url_for('main.profile'))




