# models.py - Modelos de datos y clases de usuario
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import database

class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def load_user(user_id):
        """Método estático para cargar un usuario por su ID (requerido por Flask-Login)"""
        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, name, email, role FROM users WHERE id = %s", (user_id,))
                user_data = cur.fetchone()
                if user_data:
                    return User(id=user_data[0], name=user_data[1], email=user_data[2], role=user_data[3])
                return None
            except Exception as e:
                print(f"Error loading user {user_id}: {e}")
                return None
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return None

    @staticmethod
    def create_user(name, email, password, role='cliente'):
        """Crea un nuevo usuario en la base de datos"""
        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                cur.execute("INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s) RETURNING id;", 
                           (name, email, hashed_password, role))
                user_id = cur.fetchone()[0]
                conn.commit()
                return User(id=user_id, name=name, email=email, role=role)
            except Exception as e:
                conn.rollback()
                print(f"Error al crear usuario: {e}")
                return None
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return None

    @staticmethod
    def authenticate_user(email, password):
        """Autentica un usuario por email y contraseña"""
        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id, name, email, password, role FROM users WHERE email = %s", (email,))
                user_data = cur.fetchone()
                if user_data and check_password_hash(user_data[3], password):
                    return User(id=user_data[0], name=user_data[1], email=user_data[2], role=user_data[4])
                return None
            except Exception as e:
                print(f"Error al autenticar usuario: {e}")
                return None
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return None

    @staticmethod
    def user_exists(email):
        """Verifica si un usuario ya existe por su email"""
        conn = database.get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT id FROM users WHERE email = %s", (email,))
                result = cur.fetchone()
                return result is not None
            except Exception as e:
                print(f"Error al verificar usuario: {e}")
                return False
            finally:
                if cur:
                    cur.close()
                if conn:
                    conn.close()
        return False
