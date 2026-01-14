# Guia de Deploy GRATUITO para Produção

Este guia contém instruções passo a passo para fazer deploy do sistema de reservas usando **APENAS serviços 100% gratuitos**.

## ✅ Stack GRATUITA

- **Banco de Dados**: Supabase (grátis até 500MB)
- **Backend + Frontend**: Vercel (grátis)
- **Cache/Redis**: Supabase (tem suporte nativo a Redis via Upstash gratuito)
- **Autenticação OAuth**: Google Cloud (grátis)

> **💡 Diferença chave**: O backend FastAPI será convertido em Vercel Serverless Functions (Python), eliminando a necessidade de Railway/Render.

## 📋 Checklist Pré-Deploy

- [ ] Conta Supabase criada e projeto configurado
- [ ] Conta Google Cloud com OAuth configurado
- [ ] Conta Vercel (gratuita)
- [ ] Repositório Git criado (GitHub recomendado)

---

## 🗄️ Passo 1: Configurar Supabase (Banco de Dados)

### 1.1. Criar/Verificar Projeto
1. Acesse https://supabase.com/dashboard
2. Se já tem projeto, verifique se está ativo
3. Se não tem, clique em **"New Project"**
   - Nome: `quadra-reservas` (ou similar)
   - Database Password: **Anote em lugar seguro!**
   - Region: Escolha mais próximo (ex: South America)

### 1.2. Obter Connection String
1. No projeto, vá em `Settings` → `Database`
2. Procure por **"Connection Pooling"** (não "Direct connection")
3. Mode: **Transaction**
4. Copie a string que começa com `postgresql://postgres.`
5. Substitua `[YOUR-PASSWORD]` pela senha do banco

Exemplo:
```
postgresql://postgres.xxx:senha@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

### 1.3. Habilitar Redis no Supabase (GRÁTIS!)

Boa notícia: o Supabase tem integração gratuita com Upstash Redis!

1. No Supabase Dashboard, vá em **"Integrations"**
2. Procure por **"Upstash Redis"**
3. Clique em **"Enable"** (é grátis!)
4. Copie a **Redis Connection String** (formato: `redis://default:xxx@...`)

---

## 🔐 Passo 2: Configurar Google OAuth

### 2.1. Criar Projeto Google Cloud
1. Acesse https://console.cloud.google.com/
2. Clique em criar novo projeto ou selecione existente
3. Nome: `Reservas Quadra`

### 2.2. Configurar OAuth Consent Screen
1. Menu → `APIs & Services` → `OAuth consent screen`
2. User Type: **External**
3. Preencha:
   - App name: `Reservas Quadra Condomínio`
   - User support email: seu email
   - Developer contact: seu email
4. Scopes: Não precisa adicionar nenhum extra
5. Test users: Adicione emails dos moradores (ou deixe vazio e publique depois)

### 2.3. Criar Credenciais OAuth
1. Menu → `APIs & Services` → `Credentials`
2. Clique em `Create Credentials` → `OAuth 2.0 Client ID`
3. Application type: **Web application**
4. Name: `Quadra Backend`
5. **Authorized redirect URIs** - Adicione estas URLs:
   ```
   http://localhost:3000/api/auth/callback/google
   https://SEU-APP.vercel.app/api/auth/callback/google
   ```
   ⚠️ **Importante**: Você vai atualizar a URL do Vercel depois do deploy!

6. Clique em `Create`
7. **Copie e guarde**:
   - Client ID
   - Client Secret

---

## 🔧 Passo 3: Adaptar Backend para Vercel Serverless

Como a Vercel não roda servidores persistentes (como Railway), vamos converter o FastAPI em Vercel Functions.

### 3.1. Criar estrutura para Vercel

No diretório raiz do projeto (`/home/henrique/Quadra-JP2`):

```bash
# Criar diretório api/ na raiz
mkdir -p api

# Copiar rotas do FastAPI para api/
# Cada arquivo em api/ se torna uma rota serverless
```

### 3.2. Criar `vercel.json` na raiz do projeto

Arquivo de configuração que diz à Vercel como rodar o Python:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.py",
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
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

### 3.3. Criar `requirements.txt` na raiz

```txt
fastapi
sqlalchemy
asyncpg
python-jose[cryptography]
passlib[bcrypt]
python-multipart
redis
httpx
```

> **Nota**: Vou criar scripts automatizados para fazer essa conversão!

---

## ▲ Passo 4: Deploy do Frontend + Backend na Vercel

### 4.1. Preparar Repositório Git

```bash
cd /home/henrique/Quadra-JP2

# Criar .gitignore se não existir
cat > .gitignore << EOL
.env
.env.local
.env*.local
__pycache__/
*.pyc
.venv/
venv/
node_modules/
.next/
.vercel
EOL

# Inicializar git (se ainda não foi)
git init
git add .
git commit -m "Preparando para deploy gratuito na Vercel"

# Criar repositório no GitHub
# Vá em github.com e crie um novo repositório 'quadra-reservas'

# Adicionar remote e fazer push
git remote add origin https://github.com/SEU-USUARIO/quadra-reservas.git
git branch -M main
git push -u origin main
```

### 4.2. Deploy via GitHub (Recomendado)

1. Acesse https://vercel.com/dashboard
2. Clique em **"Add New Project"**
3. Clique em **"Import Git Repository"**
4. Selecione o repositório `quadra-reservas` que acabou de criar
5. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - Deixe outras opções padrão
6. Clique em **"Deploy"**

### 4.3. Configurar Variáveis de Ambiente na Vercel

No dashboard da Vercel:
1. Vá no projeto → **Settings** → **Environment Variables**
2. Adicione as seguintes variáveis:

**Para o Frontend:**
```
NEXT_PUBLIC_API_URL=/api
```

**Para o Backend (API):**
```
DATABASE_URL=postgresql+asyncpg://postgres.xxx:senha@....pooler.supabase.com:6543/postgres
REDIS_URL=redis://default:xxx@...upstash.io:6379
JWT_SECRET=(gere com: openssl rand -hex 32)
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
FRONTEND_URL=https://seu-app.vercel.app
CORS_ORIGINS=https://seu-app.vercel.app
```

3. Para cada variável:
   - Marque **Production**, **Preview** e **Development**
   - Clique em **Save**

### 4.4. Redeploy após adicionar variáveis

1. Vá em **Deployments**
2. Clique nos 3 pontos da última deployment
3. Clique em **Redeploy**

### 4.5. Obter URL do Deploy

Após o deploy, a Vercel vai gerar uma URL como:
```
https://quadra-reservas.vercel.app
```

---

## 🔄 Passo 5: Atualizar Google OAuth com URL Real

Agora que você tem a URL do Vercel:

1. Volte no **Google Cloud Console**
2. Vá em `APIs & Services` → `Credentials`
3. Edite as credenciais OAuth criadas anteriormente
4. Em **Authorized redirect URIs**, adicione:
   ```
   https://SEU-APP-REAL.vercel.app/api/auth/callback/google
   ```
5. Clique em **Save**

---

## 🗃️ Passo 6: Aplicar Migrações no Supabase

```bash
# Na máquina local
cd /home/henrique/Quadra-JP2/backend

# Configurar temporariamente a DATABASE_URL do Supabase
export DATABASE_URL="postgresql+asyncpg://postgres.xxx:senha@...pooler.supabase.com:6543/postgres"

# Ativar ambiente virtual
source .venv/bin/activate

# Aplicar migrações
alembic upgrade head

# Seed inicial (se tiver)
python scripts/seed.py
```

---

## ✅ Passo 7: Testar Sistema Completo

### 7.1. Teste do Frontend
1. Acesse: `https://seu-app.vercel.app`
2. Deve carregar a página de login

### 7.2. Teste da API
1. Acesse: `https://seu-app.vercel.app/api/healthz`
2. Deve retornar: `{"status":"ok","version":"1.0.0"}`

### 7.3. Teste do Login com Google
1. Clique em "Entrar com Google"
2. Faça login com conta Google
3. Deve redirecionar para o dashboard

### 7.4. Verificar no Supabase
1. Acesse Supabase Dashboard
2. Vá em `Database` → `Table Editor`
3. Abra a tabela `users`
4. Verifique se o usuário foi criado

---

## 🔧 Troubleshooting

### Frontend não carrega
- Verifique logs no Vercel: Dashboard → Deployments → (sua deployment) → Logs
- Verifique se build foi bem-sucedido

### API retorna 404
- Verifique se `vercel.json` está na raiz do projeto
- Verifique se arquivos Python estão em `/api/`
- Verifique se `@vercel/python` está configurado

### Erro de CORS
- Verifique se `CORS_ORIGINS` está configurado corretamente
- Deve ser a URL exata do Vercel (ex: `https://seu-app.vercel.app`)

### Google OAuth não funciona
- Verifique se Redirect URI está correto no Google Cloud
- Deve ser: `https://seu-app.vercel.app/api/auth/callback/google`
- Verifique se Client ID e Secret estão corretos na Vercel

### Erro de conexão com banco
- Verifique se `DATABASE_URL` está configurada na Vercel
- Teste a connection string localmente: `psql "postgresql://postgres.xxx..."`
- Verifique se Supabase está ativo

---

## 📊 Monitoramento (GRÁTIS!)

### Vercel
- **Analytics**: Dashboard → Analytics (grátis!)
- **Logs**: Dashboard → Deployments → Logs
- **Performance**: Dashboard → Speed Insights

### Supabase
- **Banco de Dados**: Dashboard → Database → Table Editor
- **Logs**: Dashboard → Logs
- **API Logs**: Dashboard → API

### Google Cloud
- **OAuth Stats**: APIs & Services → Dashboard

---

## 💰 Custos (100% GRÁTIS!)

| Serviço | Plano Grátis | Limites |
|---------|--------------|---------|
| **Vercel** | Hobby (grátis) | 100GB bandwidth/mês, builds ilimitados |
| **Supabase** | Free Tier | 500MB storage, 2GB transfer/mês |
| **Upstash Redis** | Free via Supabase | 10k comandos/dia |
| **Google OAuth** | Grátis | Ilimitado |

**Total: R$ 0,00/mês** 🎉

---

## 🔄 Próximos Deploys

A Vercel faz deploy automático a cada push no GitHub!

```bash
# Fazer alterações no código
git add .
git commit -m "Minhas alterações"
git push

# A Vercel detecta automaticamente e faz deploy!
```

Para forçar redeploy:
1. Vá no dashboard da Vercel
2. Deployments → (última) → Redeploy

---

## 🌐 Domínio Customizado (Opcional, mas GRÁTIS!)

### Usar domínio próprio na Vercel
1. Comprar domínio (ex: quadracondominio.com.br) - ~R$40/ano
2. No Vercel: Settings → Domains
3. Adicionar domínio
4. Configurar DNS conforme instruções
5. SSL automático (grátis!)

### Usar subdomínio gratuito
Usar o domínio `.vercel.app` que vem de graça:
- `quadra-reservas.vercel.app`
- `quadra-jp2.vercel.app`

---

## 📝 Próximos Passos

1. [ ] Converter backend FastAPI para Vercel Functions (vou gerar scripts!)
2. [ ] Testar localmente com `vercel dev`
3. [ ] Deploy na Vercel
4. [ ] Configurar variáveis de ambiente
5. [ ] Aplicar migrações no Supabase
6. [ ] Testar sistema completo
7. [ ] Adicionar primeiros usuários

---

## 🆘 Precisa de Ajuda?

Vou criar scripts automatizados para:
1. ✅ Converter FastAPI → Vercel Functions
2. ✅ Gerar `vercel.json` automaticamente
3. ✅ Validar configuração antes do deploy
4. ✅ Aplicar migrações no Supabase

**Próximo comando**: `/criar-scripts-deploy`
