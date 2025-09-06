
# run.py - Punto de entrada principal de la aplicación
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

from app import create_app, db
## Eliminada la importación de create_tables, ya no es necesaria
from app.models import User

# Crear la instancia de la aplicación
app = create_app()

# Crear las tablas de la base de datos
with app.app_context():
    db.create_all()  # Crea tablas de SQLAlchemy
    
    # Crear usuario administrador si no existe
    if not User.query.filter_by(email='admin@planeador.com').first():
        admin = User(
            name='Administrador',
            email='admin@planeador.com',
            is_admin=True
        )
        admin.set_password('contraseña')
        db.session.add(admin)
        db.session.commit()
        print("Usuario administrador creado.")

if __name__ == '__main__':
    print("🚀 Iniciando Planeador Escolar...")
    print("📚 Aplicación organizada y modular")
    print("🌐 Servidor iniciando en http://127.0.0.1:5000")
    print("=" * 50)
    
    # Ejecutar la aplicación
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
