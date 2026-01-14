# Instruções Rápidas de Deploy

## 🚀 Resumo dos Passos

1. **Supabase** (Banco de Dados)
   - URL: https://supabase.com
   - Criar projeto → Copiar connection string
   - Adicionar `+asyncpg` na URL

2. **Google OAuth** (Autenticação)
   - URL: https://console.cloud.google.com
   - Criar credenciais OAuth 2.0
   - Redirect URI: `https://SEU-BACKEND.railway.app/api/v1/auth/callback/google`

3. **Upstash** (Redis)
   - URL: https://console.upstash.com
   - Criar database → Copiar Redis URL

4. **Railway** (Backend)
   ```bash
   npm install -g @railway/cli
   railway login
   cd backend
   railway init
   railway up
   ```
   
5. **Vercel** (Frontend)
   ```bash
   npm install -g vercel
   cd frontend
   vercel
   vercel --prod
   ```

## ⚙️ Variáveis de Ambiente Necessárias

### Railway (Backend)
```
DATABASE_URL=postgresql+asyncpg://postgres.xxx...
REDIS_URL=redis://default:xxx@upstash.io:6379
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
JWT_SECRET=openssl rand -hex 32
OAUTH_REDIRECT_URI=https://seu-backend.railway.app/api/v1/auth/callback/google
FRONTEND_URL=https://seu-app.vercel.app
CORS_ORIGINS=https://seu-app.vercel.app
```

### Vercel (Frontend)
```
NEXT_PUBLIC_API_URL=https://seu-backend.railway.app/api/v1
```

## 📚 Documentação Completa

Ver arquivo: [DEPLOY.md](./DEPLOY.md)

## ✅ Checklist Final

- [ ] Supabase configurado
- [ ] Google OAuth configurado  
- [ ] Upstash Redis criado
- [ ] Backend no Railway
- [ ] Frontend no Vercel
- [ ] Migrações aplicadas
- [ ] Testado login com Google
- [ ] URL do Railway adicionada no Google OAuth
- [ ] URLs atualizadas nas variáveis de ambiente
