# app/__init__.py - Inicialización de la aplicación Flask
import datetime
from flask import Flask
from flask_login import LoginManager
from config import Config
import os

# Inicializar Flask-Login
login_manager = LoginManager()

def format_datetime_filter(value, format='%d de %b, %H:%M'):
    """Filtro para formatear fechas de Google Calendar."""
    if not value:
        return ""
    try:
        # Google Calendar puede devolver 'dateTime' (con zona horaria) o 'date' (para eventos de todo el día)
        if 'T' in value:
            # Para dateTime, ej: '2025-08-30T10:00:00-05:00'
            # Se convierte a objeto datetime, se maneja el offset
            dt = datetime.datetime.fromisoformat(value)
        else:
            # Para date, ej: '2025-08-31'
            dt = datetime.datetime.strptime(value, '%Y-%m-%d')
            return dt.strftime('%d de %b, %Y') # Formato diferente para eventos de todo el día
        
        return dt.strftime(format)
    except (ValueError, TypeError):
        return value

def create_app(config_class=Config):
    """Application Factory Pattern para crear la instancia de Flask"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    
    app = Flask(__name__, 
                template_folder=os.path.join(project_dir, 'templates'),
                static_folder=os.path.join(project_dir, 'static'))
    
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Registrar blueprints
    from app.routes import main_bp, auth_bp
    from app.admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    
    # Configurar el user loader para Flask-Login
    from app.models import User
    login_manager.user_loader(User.load_user)

    # Registrar filtros de Jinja2
    app.jinja_env.filters['format_datetime'] = format_datetime_filter
    
    return app