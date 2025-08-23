# Configuración de la aplicación Flask
import os

class Config:
    # Configuración básica de Flask
    SECRET_KEY = 'your_secret_key_here'  # ¡CAMBIA ESTO POR UNA CLAVE SEGURA!
    
    # Configuración de la base de datos PostgreSQL
    DB_HOST = "localhost"
    DB_NAME = "planeador_escolar"
    DB_USER = "postgres"
    DB_PASSWORD = "MmateomunozV1.0"
    DB_PORT = "5432"
    
    # Configuración de la aplicación
    DEBUG = True
    
    # Configuración de Flask-Login
    LOGIN_VIEW = 'auth.login'
