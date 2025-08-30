
# run.py - Punto de entrada principal de la aplicación
from app import create_app

# Crear la instancia de la aplicación
app = create_app()

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
