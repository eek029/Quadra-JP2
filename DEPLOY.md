# Guia de Deploy para Produção

Este guia contém instruções passo a passo para fazer deploy do sistema de reservas na internet.

## 📋 Checklist Pré-Deploy

- [ ] Conta Supabase criada e projeto configurado
- [ ] Conta Google Cloud com OAuth configurado
- [ ] Repositório Git criado (GitHub recomendado)
- [ ] Contas criadas em: Vercel, Railway (ou Render), Upstash

## 🗄️ Passo 1: Configurar Supabase (Banco de Dados)

### 1.1. Criar/Verificar Projeto
1. Acesse https://supabase.com/dashboard
2. Se já tem projeto, verifique se está ativo
3. Se não tem, clique em "New Project"
   - Nome: `quadra-reservas` (ou similar)
   - Database Password: Anote em lugar seguro!
   - Region: Escolha mais próximo (ex: South America)

### 1.2. Obter Connection String
1. No projeto, vá em `Settings` → `Database`
2. Procure por **"Connection Pooling"** (não "Direct connection")
3. Mode: **Transaction**
4. Copie a string que começa com `postgresql://postgres.`
5. Substitua `[YOUR-PASSWORD]` pela senha do banco

### 1.3. Converter para AsyncPG
A string copiada estará assim:
```
postgresql://postgres.xxx:senha@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

Adicione `+asyncpg` após `postgresql`:
```
postgresql+asyncpg://postgres.xxx:senha@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

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
5. **Authorized redirect URIs** - Adicione TODAS estas URLs:
   ```
   http://localhost:8000/api/v1/auth/callback/google
   https://SEU-BACKEND.railway.app/api/v1/auth/callback/google
   ```
   ⚠️ **Importante**: Você vai atualizar a URL do Railway depois do deploy!

6. Clique em `Create`
7. **Copie e guarde**:
   - Client ID
   - Client Secret

## ⚡ Passo 3: Configurar Upstash (Redis)

1. Acesse https://console.upstash.com/
2. Crie conta (pode usar Google)
3. Clique em `Create Database`
4. Nome: `quadra-redis`
5. Region: Escolha mais próximo
6. Type: Regional (grátis)
7. Copie a **Redis URL** (formato: `redis://default:xxx@yyy.upstash.io:6379`)

## 🚂 Passo 4: Deploy do Backend (Railway)

### 4.1. Preparar Repositório
```bash
cd /home/henrique/Quadra-JP2

# Criar .gitignore se não existir
echo ".env
.env.local
__pycache__/
*.pyc
.venv/
venv/
node_modules/" > .gitignore

# Inicializar git (se ainda não foi)
git init
git add .
git commit -m "Preparando para deploy"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/SEU-USUARIO/quadra-reservas.git
git push -u origin main
```

### 4.2. Instalar Railway CLI
```bash
npm install -g @railway/cli
```

### 4.3. Fazer Deploy
```bash
# Login
railway login

# Criar projeto
railway init

# Escolha "Deploy from GitHub repo"
# Selecione o repositório que acabou de criar

# OU deploy direto do código local:
cd backend
railway up
```

### 4.4. Configurar Variáveis de Ambiente no Railway

Via CLI:
```bash
railway variables set DATABASE_URL="postgresql+asyncpg://postgres.xxx..."
railway variables set REDIS_URL="redis://default:xxx@upstash.io:6379"
railway variables set JWT_SECRET="$(openssl rand -hex 32)"
railway variables set GOOGLE_CLIENT_ID="seu-client-id"
railway variables set GOOGLE_CLIENT_SECRET="seu-secret"
railway variables set JWT_EXPIRES_IN="3600"
railway variables set CORS_ORIGINS="https://sua-app.vercel.app"
railway variables set FRONTEND_URL="https://sua-app.vercel.app"
railway variables set PROMETHEUS_ENABLED="true"
```

Ou via Dashboard:
1. Acesse https://railway.app/dashboard
2. Selecione seu projeto
3. Vá em `Variables`
4. Adicione cada variável manualmente

### 4.5. Verificar Deploy
1. Após deploy, Railway vai gerar uma URL
2. Exemplo: `https://quadra-backend-production.up.railway.app`
3. Teste o health check: `https://sua-url.railway.app/healthz`
4. Deve retornar: `{"status":"ok","version":"1.0.0"}`

### 4.6. ATUALIZAR Google OAuth Redirect URI
1. Volte no Google Cloud Console
2. Edite as credenciais OAuth
3. Adicione a URL real do Railway:
   ```
   https://SUA-URL-REAL.railway.app/api/v1/auth/callback/google
   ```

### 4.7. ATUALIZAR variável no Railway
```bash
railway variables set OAUTH_REDIRECT_URI="https://SUA-URL-REAL.railway.app/api/v1/auth/callback/google"
```

## ▲ Passo 5: Deploy do Frontend (Vercel)

### 5.1. Instalar Vercel CLI
```bash
npm install -g vercel
```

### 5.2. Fazer Deploy
```bash
cd /home/henrique/Quadra-JP2/frontend

# Login
vercel login

# Deploy (modo interativo)
vercel

# Responda as perguntas:
# - Set up and deploy? Yes
# - Which scope? Sua conta
# - Link to existing project? No
# - Project name? quadra-reservas
# - Directory? ./
# - Override settings? No
```

### 5.3. Configurar Variável de Ambiente
```bash
# Usar a URL real do Railway
vercel env add NEXT_PUBLIC_API_URL production

# Quando perguntar o valor, cole:
# https://SUA-URL-RAILWAY.railway.app/api/v1
```

### 5.4. Deploy para Produção
```bash
vercel --prod
```

### 5.5. Obter URL Final
Vercel vai gerar algo como: `https://quadra-reservas.vercel.app`

### 5.6. ATUALIZAR CORS no Backend
```bash
# Atualizar variáveis no Railway com a URL real do Vercel
railway variables set CORS_ORIGINS="https://sua-app-real.vercel.app"
railway variables set FRONTEND_URL="https://sua-app-real.vercel.app"
```

## 🗃️ Passo 6: Aplicar Migrações no Supabase

```bash
# Na pasta backend local
cd /home/henrique/Quadra-JP2/backend

# Configurar temporariamente a DATABASE_URL do Supabase
export DATABASE_URL="postgresql+asyncpg://postgres.xxx..."

# Aplicar migrações
alembic upgrade head
```

Ou via Railway:
```bash
railway run alembic upgrade head
```

## ✅ Passo 7: Testar Sistema Completo

1. **Acessar Frontend**
   - URL: https://sua-app.vercel.app
   - Deve carregar a página de login

2. **Testar Login com Google**
   - Clicar em "Entrar com Google"
   - Fazer login com conta Google
   - Deve redirecionar para dashboard

3. **Verificar Banco de Dados**
   - Acessar Supabase Dashboard
   - Ver se usuário foi criado na tabela `users`

4. **Testar Criação de Reserva**
   - (se já tiver essa funcionalidade implementada)

## 🔧 Troubleshooting

### Backend não inicia
- Verificar logs: `railway logs`
- Verificar se todas as variáveis estão configuradas
- Testar connection string do Supabase

### Frontend mostra erro 404 no login
- Verificar se `NEXT_PUBLIC_API_URL` está configurado no Vercel
- Verificar se aponta para URL correta do Railway (com `/api/v1`)

### Erro de CORS
- Verificar se `CORS_ORIGINS` no Railway está correto
- Deve ser a URL exata do Vercel (sem / no final)

### Google OAuth não funciona
- Verificar se Redirect URI está correto no Google Cloud
- Deve ser: `https://backend.railway.app/api/v1/auth/callback/google`
- Verificar se Client ID e Secret estão corretos

## 📊 Monitoramento

### Railway
- Logs: `railway logs`
- Métricas: Dashboard do Railway

### Vercel  
- Analytics: Dashboard do Vercel
- Logs: Dashboard → Deployments → Logs

### Supabase
- Dashboard → Database → Table Editor
- Logs do banco

## 💰 Custos

- Vercel: Grátis
- Railway: $5 crédito/mês (depois ~$5-10/mês)
- Supabase: Grátis até 500MB
- Upstash: Grátis até 10k req/dia
- Google OAuth: Grátis

## 🔄 Próximos Deploys

```bash
# Backend (Railway faz deploy automático ao fazer push)
git add .
git commit -m "Alterações"
git push

# Frontend
cd frontend
vercel --prod
```

## 🌐 Domínio Customizado (Opcional)

### Vercel
1. Comprar domínio (ex: quadracondominio.com)
2. No Vercel: Settings → Domains
3. Adicionar domínio
4. Configurar DNS conforme instruções

### Railway - Não suporta domínio custom no plano free
- Usar URL do Railway mesmo
- Ou usar Cloudflare Workers como proxy
