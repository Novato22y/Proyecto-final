# app/__init__.py - Inicialización de la aplicación Flask
import datetime
import os
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from config import Config
from app.database import create_database_if_not_exists

# Inicializar extensiones globalmente para que sean importables en otros módulos
db = SQLAlchemy()
login_manager = LoginManager()
oauth = OAuth()

def format_datetime_filter(value, format='%d de %b, %H:%M'):
    """Filtro para formatear fechas de Google Calendar."""
    if not value:
        return ""
    try:
        if 'T' in value:
            dt = datetime.datetime.fromisoformat(value)
        else:
            dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime('%d de %b, %Y')
        return dt.strftime(format)
    except (ValueError, TypeError):
        return value


def create_app(config_class=Config):
    """Application Factory Pattern para crear la instancia de Flask"""
    # Crear la base de datos si no existe antes de inicializar SQLAlchemy
    create_database_if_not_exists()

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)

    app = Flask(__name__, 
                template_folder=os.path.join(project_dir, 'templates'),
                static_folder=os.path.join(project_dir, 'static'))

    app.config.from_object(config_class)

    # --- Inicializar extensiones con la app ---
    db.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    login_manager.login_view = 'auth.login'

    # --- Registrar cliente OAuth de Google para Sign-In ---
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        server_metadata_url=app.config['GOOGLE_DISCOVERY_URL'],
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
    
    # --- Configurar el user loader para Flask-Login ---
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # Se usa el nuevo modelo SQLAlchemy para cargar el usuario por su ID
        return User.query.get(int(user_id))

    # --- Registrar Blueprints ---
    from app.routes import main_bp, auth_bp
    from app.admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # --- Registrar filtros de Jinja2 ---
    app.jinja_env.filters['format_datetime'] = format_datetime_filter
    
    return app
