#!/bin/bash
##
# Script para validar configuração antes do deploy
# Uso: bash scripts/validate_deploy.sh
##

# set -e (removido para não abortar em falhas de validação)

echo "🔍 Validando configuração para deploy na Vercel..."
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de erros
ERRORS=0
WARNINGS=0

# Função para verificar arquivo
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 encontrado${NC}"
    else
        echo -e "${RED}❌ $1 NÃO encontrado${NC}"
        ((ERRORS++))
    fi
}

# Função para verificar diretório
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ Diretório $1 encontrado${NC}"
    else
        echo -e "${RED}❌ Diretório $1 NÃO encontrado${NC}"
        ((ERRORS++))
    fi
}

# Função para avisos
warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

echo "📂 Verificando estrutura de arquivos..."
check_file "vercel.json"
check_file "requirements.txt"
check_file ".env.example"
check_file ".gitignore"
check_dir "api"
check_file "api/index.py"
check_dir "frontend"
check_file "frontend/package.json"
check_dir "backend"
check_file "backend/main.py"

echo ""
echo "🔐 Verificando variáveis de ambiente..."

# Verificar se .env existe (não deve estar no git!)
if [ -f ".env" ]; then
    warn ".env encontrado - CERTIFIQUE-SE de que está no .gitignore!"
fi

# Verificar se .env.example tem todas as variáveis
REQUIRED_VARS=(
    "DATABASE_URL"
    "REDIS_URL"
    "JWT_SECRET"
    "GOOGLE_CLIENT_ID"
    "GOOGLE_CLIENT_SECRET"
    "FRONTEND_URL"
    "CORS_ORIGINS"
)

if [ -f ".env.example" ]; then
    for var in "${REQUIRED_VARS[@]}"; do
        if grep -q "$var" .env.example; then
            echo -e "${GREEN}✅ $var está no .env.example${NC}"
        else
            echo -e "${RED}❌ $var NÃO está no .env.example${NC}"
            ((ERRORS++))
        fi
    done
fi

echo ""
echo "📦 Verificando dependências Python..."

if [ -f "requirements.txt" ]; then
    REQUIRED_PACKAGES=(
        "fastapi"
        "sqlalchemy"
        "asyncpg"
        "python-jose"
        "mangum"
        "redis"
    )
    
    for pkg in "${REQUIRED_PACKAGES[@]}"; do
        if grep -qi "$pkg" requirements.txt; then
            echo -e "${GREEN}✅ $pkg está no requirements.txt${NC}"
        else
            echo -e "${RED}❌ $pkg NÃO está no requirements.txt${NC}"
            ((ERRORS++))
        fi
    done
fi

echo ""
echo "📦 Verificando dependências Node.js..."

if [ -f "frontend/package.json" ]; then
    if grep -q "next" frontend/package.json; then
        echo -e "${GREEN}✅ Next.js configurado${NC}"
    else
        warn "Next.js não encontrado no package.json"
    fi
fi

echo ""
echo "🔧 Verificando vercel.json..."

if [ -f "vercel.json" ]; then
    if grep -q "@vercel/python" vercel.json; then
        echo -e "${GREEN}✅ @vercel/python configurado${NC}"
    else
        echo -e "${RED}❌ @vercel/python NÃO configurado${NC}"
        ((ERRORS++))
    fi
    
    if grep -q "@vercel/next" vercel.json; then
        echo -e "${GREEN}✅ @vercel/next configurado${NC}"
    else
        warn "@vercel/next não configurado"
    fi
fi

echo ""
echo "📊 Verificando .gitignore..."

if [ -f ".gitignore" ]; then
    IGNORE_ITEMS=(
        ".env"
        "__pycache__"
        "node_modules"
        ".next"
        ".vercel"
    )
    
    for item in "${IGNORE_ITEMS[@]}"; do
        if grep -q "$item" .gitignore; then
            echo -e "${GREEN}✅ $item está no .gitignore${NC}"
        else
            warn "$item não está no .gitignore"
        fi
    done
fi

echo ""
echo "═══════════════════════════════════════"
echo "📋 RESUMO DA VALIDAÇÃO"
echo "═══════════════════════════════════════"

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✅ Tudo certo! Pronto para deploy!${NC}"
    echo ""
    echo "Próximos passos:"
    echo "1. Fazer commit: git add . && git commit -m \"Preparando para deploy\""
    echo "2. Fazer push: git push"
    echo "3. Conectar no Vercel Dashboard: https://vercel.com/dashboard"
    echo "4. Importar repositório GitHub"
    echo "5. Configurar variáveis de ambiente"
    echo "6. Deploy! 🚀"
    exit 0
elif [ $ERRORS -eq 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS avisos encontrados (pode continuar)${NC}"
    exit 0
else
    echo -e "${RED}❌ $ERRORS erros encontrados! Corrija antes do deploy.${NC}"
    echo -e "${YELLOW}⚠️  $WARNINGS avisos${NC}"
    exit 1
fi
