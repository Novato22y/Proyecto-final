# utils.py - Funciones utilitarias
from werkzeug.security import generate_password_hash
import database

def create_admin_user():
    """Crea el usuario administrador por defecto"""
    conn = database.get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            # Verificar si el administrador ya existe por correo electrónico
            admin_email = 'admin@planeador.com'
            cur.execute("SELECT id FROM users WHERE email = %s", (admin_email,))
            existing_admin = cur.fetchone()

            if existing_admin:
                print("El usuario administrador ya existe.")
                return

            # Crear contraseña hasheada para el administrador
            admin_password_raw = 'admin_password_segura_123'  # ¡CAMBIA ESTO POR UNA CONTRASEÑA FUERTE!
            hashed_admin_password = generate_password_hash(admin_password_raw, method='pbkdf2:sha256')

            # Insertar el usuario administrador
            cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;",
                        ('Administrador', admin_email, hashed_admin_password, 'administrador'))
            admin_id = cur.fetchone()[0]
            conn.commit()
            
            print("\n")
            print("----------------------------------------------------")
            print("¡Usuario administrador creado exitosamente!")
            print(f"ID: {admin_id}")
            print(f"Nombre: Administrador")
            print(f"Correo: {admin_email}")
            print(f"Contraseña (plano, ¡CÁMBIALA INMEDIATAMENTE!): {admin_password_raw}")
            print(f"Rol: administrador")
            print("----------------------------------------------------")
            print("\n")
        except Exception as e:
            conn.rollback()
            print(f"Error al crear el usuario administrador: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

def initialize_database():
    """Inicializa la base de datos creando las tablas y el usuario administrador"""
    print("Inicializando base de datos...")
    database.create_table()
    create_admin_user()
    print("Base de datos inicializada correctamente.")
