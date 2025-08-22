# app_new.py - Aplicación principal Flask simplificada
from flask import Flask
from flask_login import LoginManager
from config import SECRET_KEY, DEBUG, HOST, PORT
from models import User
from routes import init_routes
from utils import initialize_database

def create_app():
    """Factory function para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Callback para cargar usuarios (requerido por Flask-Login)"""
        return User.load_user(user_id)
    
    # Inicializar todas las rutas
    init_routes(app)
    
    return app

if __name__ == '__main__':
    # Crear la aplicación
    app = create_app()
    
    # Inicializar la base de datos
    with app.app_context():
        initialize_database()
    
    # Ejecutar la aplicación
    app.run(debug=DEBUG, host=HOST, port=PORT)
