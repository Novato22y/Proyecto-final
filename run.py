
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
    # Asegurarse de que la columna 'music' exista en la tabla pomodoro_presets (solo desarrollo)
    try:
        from sqlalchemy import text
        inspector = db.inspect(db.engine)
        cols = [c['name'] for c in inspector.get_columns('pomodoro_presets')]
        if 'music' not in cols:
            print("Columna 'music' no existe en 'pomodoro_presets'. Creando columna...")
            dialect = db.engine.dialect.name
            alter_sql = 'ALTER TABLE pomodoro_presets ADD COLUMN music TEXT'
            # Ejecutar con conexión
            with db.engine.begin() as conn:
                conn.execute(text(alter_sql))
            print("Columna 'music' añadida.")
    except Exception as e:
        print('No se pudo asegurar la columna music:', e)

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
