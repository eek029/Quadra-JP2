#!/usr/bin/env python3
"""
Script para converter o backend FastAPI para Vercel Serverless Functions.
Uso: python scripts/convert_to_vercel.py
"""

import os
import shutil
from pathlib import Path

# Diretórios
ROOT_DIR = Path(__file__).parent.parent
BACKEND_DIR = ROOT_DIR / "backend"
API_DIR = ROOT_DIR / "api"

def create_api_directory():
    """Cria o diretório api/ na raiz se não existir."""
    if API_DIR.exists():
        print(f"⚠️  Diretório {API_DIR} já existe. Removendo...")
        shutil.rmtree(API_DIR)
    
    API_DIR.mkdir(parents=True)
    print(f"✅ Diretório {API_DIR} criado")

def create_vercel_json():
    """Cria o arquivo vercel.json na raiz do projeto."""
    vercel_config = """{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
"""
    
    vercel_json_path = ROOT_DIR / "vercel.json"
    with open(vercel_json_path, "w") as f:
        f.write(vercel_config)
    
    print(f"✅ Arquivo {vercel_json_path} criado")

def create_requirements_txt():
    """Cria requirements.txt na raiz do projeto."""
    requirements = """fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
asyncpg==0.29.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
redis==5.0.1
httpx==0.25.1
alembic==1.12.1
pydantic==2.5.0
pydantic-settings==2.1.0
"""
    
    requirements_path = ROOT_DIR / "requirements.txt"
    with open(requirements_path, "w") as f:
        f.write(requirements)
    
    print(f"✅ Arquivo {requirements_path} criado")

def create_api_index():
    """Cria o arquivo api/index.py que será o entry point para Vercel."""
    api_index = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import os

# Importar routers do backend
import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app.main import app as fastapi_app

# Handler para Vercel
handler = Mangum(fastapi_app)

# Para desenvolvimento local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000)
"""
    
    api_index_path = API_DIR / "index.py"
    with open(api_index_path, "w") as f:
        f.write(api_index)
    
    print(f"✅ Arquivo {api_index_path} criado")

def update_requirements_with_mangum():
    """Adiciona mangum ao requirements.txt."""
    requirements_path = ROOT_DIR / "requirements.txt"
    
    with open(requirements_path, "a") as f:
        f.write("mangum==0.17.0\n")
    
    print(f"✅ Adicionado 'mangum' ao requirements.txt")

def create_env_example():
    """Cria arquivo .env.example com as variáveis necessárias."""
    env_example = """# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Redis
REDIS_URL=redis://default:password@host:port

# JWT
JWT_SECRET=your-secret-key-here-use-openssl-rand-hex-32
JWT_EXPIRES_IN=3600

# Google OAuth
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
OAUTH_REDIRECT_URI=https://your-app.vercel.app/api/auth/callback/google

# Frontend
FRONTEND_URL=https://your-app.vercel.app
CORS_ORIGINS=https://your-app.vercel.app

# Observabilidade (opcional)
PROMETHEUS_ENABLED=true
"""
    
    env_example_path = ROOT_DIR / ".env.example"
    with open(env_example_path, "w") as f:
        f.write(env_example)
    
    print(f"✅ Arquivo {env_example_path} criado")

def create_gitignore():
    """Atualiza .gitignore."""
    gitignore_content = """.env
.env.local
.env*.local
__pycache__/
*.pyc
*.pyo
*.pyd
.venv/
venv/
env/
node_modules/
.next/
.vercel
*.log
.DS_Store
.idea/
.vscode/
*.swp
*.swo
dist/
build/
"""
    
    gitignore_path = ROOT_DIR / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    
    print(f"✅ Arquivo {gitignore_path} atualizado")

def main():
    """Executa a conversão completa."""
    print("🚀 Iniciando conversão do backend FastAPI para Vercel Serverless...\n")
    
    # 1. Criar estrutura de diretórios
    create_api_directory()
    
    # 2. Criar arquivos de configuração
    create_vercel_json()
    create_requirements_txt()
    create_api_index()
    update_requirements_with_mangum()
    
    # 3. Criar arquivos auxiliares
    create_env_example()
    create_gitignore()
    
    print("\n✅ Conversão concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Instale o Mangum: pip install mangum")
    print("2. Teste localmente: cd api && python index.py")
    print("3. Ou use: vercel dev (requer Vercel CLI)")
    print("4. Configure as variáveis de ambiente no .env")
    print("5. Faça deploy: vercel --prod")
    print("\n💡 Veja o arquivo DEPLOY.md para instruções completas!")

if __name__ == "__main__":
    main()
