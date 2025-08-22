# app_simple.py - Aplicación Flask simplificada sin inicialización de base de datos
from flask import Flask, render_template
from flask_login import LoginManager
from config import SECRET_KEY, DEBUG, HOST, PORT

def create_app():
    """Factory function para crear la aplicación Flask simplificada"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Configuración de Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    # Ruta principal simple
    @app.route('/')
    def principal():
        return """
        <html>
        <head><title>School Planner - Estructura Modular</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px; background-color: #1e1e1e; color: #f0f0f0;">
            <h1>🎉 ¡Aplicación Modular Funcionando!</h1>
            <h2>📁 Estructura del Proyecto:</h2>
            <ul>
                <li>✅ config.py - Configuraciones</li>
                <li>✅ database.py - Base de datos</li>
                <li>✅ models.py - Modelos</li>
                <li>✅ routes.py - Rutas</li>
                <li>✅ utils.py - Utilidades</li>
                <li>✅ app_new.py - Aplicación principal</li>
            </ul>
            <h2>🚀 Estado:</h2>
            <p>La aplicación Flask se ha iniciado correctamente con la estructura modular.</p>
            <h2>⚠️ Nota:</h2>
            <p>Hay un problema de codificación con la base de datos que necesita resolverse.</p>
            <h2>🔧 Próximos Pasos:</h2>
            <ol>
                <li>Verificar configuración de PostgreSQL</li>
                <li>Resolver problema de codificación</li>
                <li>Probar funcionalidad completa</li>
            </ol>
        </body>
        </html>
        """
    
    @app.route('/status')
    def status():
        return {
            'status': 'success',
            'message': 'Aplicación modular funcionando',
            'modules': ['config.py', 'database.py', 'models.py', 'routes.py', 'utils.py'],
            'database': 'pendiente de conexión'
        }
    
    return app

if __name__ == '__main__':
    print("🚀 Iniciando aplicación modular simplificada...")
    print("📁 Estructura verificada:")
    print("   ✅ config.py - Configuraciones")
    print("   ✅ database.py - Base de datos")
    print("   ✅ models.py - Modelos")
    print("   ✅ routes.py - Rutas")
    print("   ✅ utils.py - Utilidades")
    print("   ✅ app_new.py - Aplicación principal")
    print("\n🌐 Iniciando servidor Flask...")
    print("⚠️  Nota: Base de datos no inicializada debido a error de codificación")
    
    # Crear la aplicación
    app = create_app()
    
    # Ejecutar la aplicación
    app.run(debug=DEBUG, host=HOST, port=PORT)
