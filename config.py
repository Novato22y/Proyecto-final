# config.py - Archivo de Configuración de la aplicación Flask
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde un archivo .env.
# Python buscará un archivo llamado .env en el directorio del proyecto y cargará las variables definidas ahí.
load_dotenv()

class Config:
    """
    Clase de configuración para la aplicación Flask.
    Define las variables que la aplicación necesita para funcionar.
    Los valores se cargan desde variables de entorno para mayor seguridad y flexibilidad.
    NO DEBES ESCRIBIR VALORES SECRETOS DIRECTAMENTE AQUÍ.
    """

    # --- Configuración General de Flask ---

    # SECRET_KEY: Una clave secreta para proteger las sesiones de usuario y otros datos.
    # Es fundamental para la seguridad. El valor se carga desde el archivo .env.
    # En tu archivo .env, deberías tener una línea como: SECRET_KEY='una-cadena-de-texto-muy-larga-y-aleatoria'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key_for_development')

    # DEBUG: Activa o desactiva el modo de depuración de Flask.
    # Cuando está en True, Flask mostrará errores detallados en el navegador.
    # Debería ser False en un entorno de producción.
    DEBUG = True

    # --- Configuración de la Base de Datos (PostgreSQL) ---
    # Estas variables le dicen a la aplicación cómo conectarse a tu base de datos.
    # Todos los valores se cargan desde tu archivo .env.
    # Ejemplo de lo que deberías tener en tu archivo .env:
    # DB_HOST=localhost
    # DB_NAME=planeador_escolar
    # DB_USER=postgres
    # DB_PASSWORD=tu_contraseña
    # DB_PORT=5432

    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'planeador_escolar')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT', '5432')

    # --- Configuración de Autenticación (Flask-Login) ---

    # LOGIN_VIEW: La ruta a la que se redirigirá a los usuarios si intentan acceder
    # a una página protegida sin haber iniciado sesión. 'auth.login' se refiere
    # al blueprint 'auth' y la ruta 'login'.
    LOGIN_VIEW = 'auth.login'

    # --- Credenciales de APIs Externas (Google OAuth: Calendar & Sign-In) ---
    # Aquí se cargan las credenciales para las APIs de Google.
    # NUNCA escribas el ID o el secreto del cliente directamente en este archivo.
    # Deben estar en tu archivo .env.
    # Ejemplo en .env:
    # GOOGLE_CLIENT_ID='tu-id-de-cliente-de-google.apps.googleusercontent.com'
    # GOOGLE_CLIENT_SECRET='tu-secreto-de-cliente-de-google'
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

    # GOOGLE_DISCOVERY_URL: URL de descubrimiento de OpenID de Google.
    # Authlib la usa para encontrar automáticamente las URLs de autorización,
    # token y userinfo, simplificando la configuración.
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
