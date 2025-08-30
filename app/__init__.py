# app/__init__.py - Inicialización de la aplicación Flask
from flask import Flask
from flask_login import LoginManager
from config import Config
import os

# Inicializar Flask-Login
login_manager = LoginManager()

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
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Configurar el user loader para Flask-Login
    from app.models import User
    login_manager.user_loader(User.load_user)
    
    return app
