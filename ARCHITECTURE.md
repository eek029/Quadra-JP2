# Arquitetura do Sistema

## Visão Geral

O sistema segue uma arquitetura cliente-servidor moderna, desacoplada, utilizando REST API para comunicação.

## Diagrama de Componentes

\`\`\`mermaid
graph TD
    Client[Browser / Next.js]
    LB[Load Balancer / Nginx]
    API[FastAPI Backend]
    DB[(PostgreSQL)]
    Cache[(Redis)]
    Worker[RQ Worker]
    Ext[Google Auth / Twilio]

    Client -->|HTTPS| API
    API -->|Read/Write| DB
    API -->|Queue Jobs| Cache
    Worker -->|Consume Jobs| Cache
    Worker -->|Send SMS| Ext
    API -->|OIDC| Ext
\`\`\`

## Fluxos Principais

### Autenticação
1. Usuário clica em "Entrar com Google".
2. Backend gera URL de autorização e redireciona (ou retorna para o frontend redirecionar).
3. Google valida usuário e retorna código para callback do Backend.
4. Backend troca código por tokens, cria/atualiza usuário no DB.
5. Backend gera JWT e redireciona para o Frontend com token.

### Reservas
1. Frontend solicita slots disponíveis.
2. Backend consulta DB e verifica overlaps/blackouts.
3. Usuário submete reserva.
4. Backend valida regras (máx 2/dia, etc).
5. Se válido, salva status PENDING (ou CONFIRMED dependendo da regra).
6. Job de notificação é enfileirado no Redis.

## Decisões Técnicas

- **FastAPI**: Escolhido pela performance (async), tipagem forte (Pydantic) e facilidade de documentação (OpenAPI).
- **SQLAlchemy 2.0 (Async)**: Para operações não-bloqueantes no banco de dados.
- **Next.js 14**: Server Components para performance e SEO, App Router para organização.
- **Tailwind + Headless UI**: Desenvolvimento rápido de UI acessível e bonita.
- **Supabase (PostgreSQL)**: Facilita gestão, backups e escalabilidade do banco.
