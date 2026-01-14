# 🚀 Deploy Rápido (100% Gratuito)

Guia resumido para fazer deploy em **5 minutos** usando apenas Supabase + Vercel.

---

## ⚡ TL;DR (Versão Super Rápida)

```bash
# 1. Converter para Vercel
python scripts/convert_to_vercel.py

# 2. Validar configuração
bash scripts/validate_deploy.sh

# 3. Subir para GitHub
git add .
git commit -m "Deploy inicial"
git push

# 4. Deploy na Vercel (via dashboard)
# Vá em https://vercel.com/dashboard
# Importe o repositório GitHub
# Configure variáveis de ambiente
# Deploy! 🎉
```

---

## 📝 Checklist de 5 Minutos

### 1️⃣ Preparar Supabase (2 min)

- [ ] Criar projeto no Supabase: https://supabase.com/dashboard
- [ ] Copiar **Connection String** (Transaction mode)
- [ ] Habilitar Redis gratuito (Integrations → Upstash Redis)
- [ ] Copiar **Redis URL**

### 2️⃣ Configurar Google OAuth (2 min)

- [ ] Criar projeto: https://console.cloud.google.com
- [ ] OAuth Consent Screen → External
- [ ] Criar credenciais OAuth 2.0
- [ ] Redirect URI: `https://SEU-APP.vercel.app/api/auth/callback/google`
- [ ] Copiar **Client ID** e **Client Secret**

### 3️⃣ Converter e Validar (30 seg)

```bash
python scripts/convert_to_vercel.py
bash scripts/validate_deploy.sh
```

### 4️⃣ Subir para GitHub (30 seg)

```bash
git init
git add .
git commit -m "Deploy inicial"
git remote add origin https://github.com/SEU-USUARIO/quadra-reservas.git
git push -u origin main
```

### 5️⃣ Deploy na Vercel (1 min)

1. Acesse: https://vercel.com/dashboard
2. **Add New Project** → **Import Git Repository**
3. Selecione o repositório
4. **Framework**: Next.js
5. **Root Directory**: `frontend`
6. **Deploy**

### 6️⃣ Configurar Variáveis (1 min)

No Vercel Dashboard → Settings → Environment Variables:

**Frontend:**
```
NEXT_PUBLIC_API_URL=/api
```

**Backend:**
```
DATABASE_URL=postgresql+asyncpg://postgres.xxx:senha@...pooler.supabase.com:6543/postgres
REDIS_URL=redis://default:xxx@...upstash.io:6379
JWT_SECRET=cole-o-resultado-de-openssl-rand-hex-32-aqui
GOOGLE_CLIENT_ID=seu-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
FRONTEND_URL=https://seu-app.vercel.app
CORS_ORIGINS=https://seu-app.vercel.app
```

Clique em **Save** → **Redeploy**

### 7️⃣ Atualizar Google OAuth (30 seg)

Volte no Google Cloud Console e adicione a URL REAL do Vercel:
```
https://sua-app-real.vercel.app/api/auth/callback/google
```

### 8️⃣ Aplicar Migrações (30 seg)

```bash
cd backend
export DATABASE_URL="postgresql+asyncpg://postgres.xxx..."
alembic upgrade head
```

---

## ✅ Pronto!

Acesse: `https://sua-app.vercel.app`

---

## 🆘 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| **Build falhou** | Verifique logs no Vercel Dashboard → Deployments |
| **API retorna 404** | Verifique se `api/index.py` existe |
| **Login não funciona** | Verifique Redirect URI no Google Cloud |
| **Erro de CORS** | Verifique `CORS_ORIGINS` na Vercel |

---

## 📚 Guia Completo

Para mais detalhes, veja: [DEPLOY.md](./DEPLOY.md)

---

## 💰 Isso é MESMO gratuito?

✅ SIM! **R$ 0,00/mês**

- Vercel: Grátis ✅
- Supabase: Grátis até 500MB ✅
- Upstash Redis: Grátis via Supabase ✅
- Google OAuth: Grátis ✅

---

## 🔄 Próximos Deploys

Deploy automático a cada `git push`! 🎉

```bash
git add .
git commit -m "Minhas alterações"
git push
```

A Vercel detecta e faz deploy automaticamente!
