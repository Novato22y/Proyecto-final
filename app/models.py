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
