# app_test.py - Versión de prueba sin dependencias de base de datos
from flask import Flask, render_template
from flask_login import LoginManager
from config import SECRET_KEY, DEBUG, HOST, PORT

def create_app():
    """Factory function para crear la aplicación Flask de prueba"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Ruta de prueba simple
    @app.route('/')
    def principal():
        return "¡Aplicación modular funcionando correctamente! 🎉"
    
    @app.route('/test')
    def test():
        return "Módulo de rutas funcionando ✅"
    
    return app

if __name__ == '__main__':
    print("🚀 Iniciando aplicación de prueba...")
    print("📁 Estructura modular verificada:")
    print("   ✅ config.py - Configuraciones")
    print("   ✅ database.py - Base de datos")
    print("   ✅ models.py - Modelos")
    print("   ✅ routes.py - Rutas")
    print("   ✅ utils.py - Utilidades")
    print("   ✅ app_new.py - Aplicación principal")
    print("\n🌐 Iniciando servidor Flask...")
    
    # Crear la aplicación
    app = create_app()
    
    # Ejecutar la aplicación
    app.run(debug=DEBUG, host=HOST, port=PORT)
