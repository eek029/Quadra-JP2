# App de Reservas da Quadra do Condomínio

Sistema completo para gestão de reservas da quadra, com autenticação Google, regras de negócios complexas (limites, blackouts) e notificações.

## Tecnologias

- **Backend**: FastAPI, SQLAlchemy, Alembic, Redis, RQ.
- **Frontend**: Next.js 14 (App Router), Tailwind CSS, Headless UI.
- **Banco de Dados**: PostgreSQL (Supabase compatível).
- **Infraestrutura**: Docker Compose.

## Pré-requisitos

- Docker e Docker Compose
- Node.js 18+ (para rodar local sem Docker)
- Python 3.11+ (para rodar local sem Docker)

## Configuração Rápida

1. Clone o repositório.
2. Copie o arquivo de exemplo de variáveis:
   ```bash
   cp .env.example .env
   ```
3. Preencha o `.env` com suas credenciais (Google OAuth, Banco de Dados, etc).
   - Se usar Supabase, use a connection string fornecida no painel.

4. Inicie o ambiente cmo Docker:
   ```bash
   ./setup.sh
   # ou
   docker compose up -d --build
   ```

5. Aplique as migrações (com o container rodando):
   ```bash
   docker compose exec backend alembic upgrade head
   ```

## Rodando Localmente (Sem Docker)

Se não tiver Docker, você pode rodar os serviços individualmente.

### Backend

1. Instale dependências:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Configure o `.env` na raiz.
3. Inicie o servidor:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend

1. Instale dependências:
   ```bash
   cd frontend
   npm install
   ```
2. Inicie o servidor:
   ```bash
   npm run dev
   ```

## Documentação da API

Acesse `http://localhost:8000/api/docs` para ver a documentação interativa (Swagger UI).

## Estrutura do Projeto

- `/backend`: Código fonte da API em Python.
- `/frontend`: Código fonte da aplicação web em Next.js.
- `/scripts`: Scripts auxiliares.

## Observações Importantes

- A autenticação requer credenciais válidas do Google Cloud Console.
- O sistema de notificações usa Twilio.
