# app/models.py - Modelos de datos de la aplicación
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db # Importar la instancia de SQLAlchemy

class User(UserMixin, db.Model):
    """Modelo de usuario para la base de datos, compatible con SQLAlchemy y Flask-Login."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=True) # Nullable para usuarios de OAuth y permite hashes largos
    name = db.Column(db.String(100), nullable=False)
    
    # Campo para el rol del usuario. True si es admin.
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # --- Nuevo campo para Google Sign-In ---
    google_id = db.Column(db.String(120), unique=True, nullable=True, index=True)

    # Foto de perfil personalizada
    profile_image = db.Column(db.String(255), nullable=True)

    def set_password(self, password):
        """Crea un hash de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica el hash de la contraseña."""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'

# Modelo de Tarea (evolución del Recordatorio)
class Tarea(db.Model):
    """Modelo de tarea para la gestión completa de tareas con Kanban."""
    __tablename__ = 'tareas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.Date, nullable=True)  # Ahora es nulable para tareas sin fecha
    importancia = db.Column(db.String(20), nullable=True)  # Ahora es nulable
    asunto = db.Column(db.String(100), nullable=True)  # Para categorizar: "Colegio", "Vida", "Trabajo"
    status = db.Column(db.String(20), nullable=False, default='inbox')  # 'inbox', 'incompleta', 'completa'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Relaciones
    enlaces = db.relationship('Enlace', backref='tarea', lazy=True, cascade='all, delete-orphan')
    contactos = db.relationship('Contacto', backref='tarea', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='tareas')
    
    def __repr__(self):
        return f'<Tarea {self.titulo}>'
    
    def to_dict(self):
        """Convierte la tarea a diccionario para JSON."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'importancia': self.importancia,
            'asunto': self.asunto,
            'status': self.status,
            'enlaces': [enlace.to_dict() for enlace in self.enlaces],
            'contactos': [contacto.to_dict() for contacto in self.contactos],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Enlace(db.Model):
    """Modelo para almacenar URLs asociadas a una tarea."""
    __tablename__ = 'enlaces'
    
    id = db.Column(db.Integer, primary_key=True)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    titulo = db.Column(db.String(200), nullable=True)  # Título descriptivo del enlace
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Enlace {self.url}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'titulo': self.titulo,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Contacto(db.Model):
    """Modelo para almacenar contactos asociados a una tarea."""
    __tablename__ = 'contactos'
    
    id = db.Column(db.Integer, primary_key=True)
    tarea_id = db.Column(db.Integer, db.ForeignKey('tareas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    telefono = db.Column(db.String(20), nullable=True)
    notas = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Contacto {self.nombre}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'telefono': self.telefono,
            'notas': self.notas,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Mantener el modelo Recordatorio para compatibilidad
class Recordatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Si usas usuarios
    fecha = db.Column(db.String(10), nullable=False)  # Formato 'YYYY-MM-DD'
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    importancia = db.Column(db.String(10), nullable=False, default='baja')


# Presets para Pomodoro por usuario
class PomodoroPreset(db.Model):
    __tablename__ = 'pomodoro_presets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    work = db.Column(db.Integer, nullable=False, default=25)
    short = db.Column(db.Integer, nullable=False, default=5)
    long = db.Column(db.Integer, nullable=False, default=15)
    color_work = db.Column(db.String(7), nullable=True)
    color_short = db.Column(db.String(7), nullable=True)
    color_long = db.Column(db.String(7), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='pomodoro_presets')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'work': self.work,
            'short': self.short,
            'long': self.long,
            'colors': {
                'work': self.color_work,
                'short': self.color_short,
                'long': self.color_long
            },
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

