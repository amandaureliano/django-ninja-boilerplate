# django-ninja-boilerplate

Stack: Django 6 · Django Ninja · PostgreSQL · Python 3.14 · uv · Granian · Google SSO

## Requisitos

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)
- Docker (para o banco de dados)

## Setup

```bash
# 1. Dependências
uv sync --all-groups

# 2. Variáveis de ambiente
cp .env.example .env

# 3. Banco de dados
docker compose up -d db

# 4. Migrações e superusuário
make migrate
uv run python app/manage.py createsuperuser

# 5. Hooks de pré-commit
uv run pre-commit install
```

## Comandos

```bash
make run          # http://localhost:8000
make test         # roda os testes
make coverage     # testes + relatório de cobertura
make migrate      # aplica migrações
make migrations   # gera novas migrações
make shell        # Django shell
make lint         # ruff check
make format       # ruff format
```

## API

Documentação interativa disponível em **`/api/docs`** (Swagger UI).

| Método | Endpoint                  | Auth   | Descrição                       |
|--------|---------------------------|--------|---------------------------------|
| GET    | `/api/health`             | —      | Health check                    |
| POST   | `/api/auth/token`         | —      | Obtém access + refresh token    |
| POST   | `/api/auth/token/refresh` | —      | Renova access token             |
| POST   | `/api/auth/social/google` | —      | Login via Google (access token) |
| GET    | `/api/users/me`           | Bearer | Perfil do usuário autenticado   |

### Google SSO

**Fluxo web (redirect OAuth):**
```
GET /auth/login/google-oauth2/
```

**Fluxo API (SPA/mobile):** envie o access token do Google para `/api/auth/social/google` e receba os tokens JWT do sistema.

Para ativar, configure no `.env`:
```
GOOGLE_OAUTH2_KEY=seu-client-id
GOOGLE_OAUTH2_SECRET=seu-client-secret
```
Credenciais em [console.cloud.google.com](https://console.cloud.google.com) → APIs & Services → Credentials.

## Estrutura

```
app/
├── apps/
│   ├── core/              # Infraestrutura transversal
│   │   ├── auth.py        # JWTAuth + helpers de token
│   │   ├── exceptions.py  # AppError
│   │   ├── models.py      # BaseModel (uuid, timestamps)
│   │   ├── schemas.py     # Schemas de autenticação
│   │   └── api.py         # Endpoints de auth e Google SSO
│   └── users/             # Feature: usuários
│       ├── models.py      # User (AbstractUser customizado)
│       ├── schemas.py     # UserOut
│       ├── api.py         # GET /users/me
│       └── views.py       # Views HTML (hybrid)
├── config/
│   ├── settings.py
│   ├── api.py             # NinjaAPI + exception handlers
│   └── urls.py
└── templates/
tests/
├── factories/             # Factories para testes
├── conftest.py
├── test_auth.py
└── test_users.py
```

## Variáveis de ambiente

Veja [`.env.example`](.env.example) para a lista completa.
