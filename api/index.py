from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

# Importar routers do backend
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

try:
    from main import app as fastapi_app
except ImportError:
    # Tentar estrutura alternativa caso main esteja dentro de app/
    try:
        from app.main import app as fastapi_app
    except ImportError:
        print("❌ Erro: Não foi possível encontrar 'app' em main.py ou app/main.py")
        raise

# Handler para Vercel
handler = Mangum(fastapi_app)

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
