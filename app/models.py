# app/models.py - Modelos de datos de la aplicación
from flask_login import UserMixin

class User(UserMixin):
    """Modelo de usuario para Flask-Login"""
    
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

    @staticmethod
    def load_user(user_id):
        """Método estático para cargar un usuario por su ID (requerido por Flask-Login)"""
        from app.database import get_db_connection
        
        conn = get_db_connection()
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
