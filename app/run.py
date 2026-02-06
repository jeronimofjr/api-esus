import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app

app = create_app()


if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    print("📡 API disponível em: http://localhost:8001")
    print("📚 Documentação: http://localhost:8001/")
    
    app.run(
        host="0.0.0.0",
        port=8001,
        debug=True
    )