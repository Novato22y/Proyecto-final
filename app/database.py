# app/database.py - Funciones de conexión y operaciones con la base de datos

import psycopg2
from config import Config

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_db_connection():
    """Establece una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT,
            options=f"-c client_encoding=UTF8"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def create_database_if_not_exists():
    """Crea la base de datos PostgreSQL si no existe."""
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            host=Config.DB_HOST,
            port=Config.DB_PORT
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{Config.DB_NAME}'")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f'CREATE DATABASE {Config.DB_NAME}')
            print(f"Base de datos '{Config.DB_NAME}' creada exitosamente.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
