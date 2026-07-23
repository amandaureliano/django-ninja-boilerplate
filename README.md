# Novo Projeto

Stack: Django 6 · Django Ninja · PostgreSQL · Python 3.14 · uv

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

| Método | Endpoint              | Auth     | Descrição               |
|--------|-----------------------|----------|-------------------------|
| GET    | `/api/health`         | —        | Health check            |
| POST   | `/api/auth/token`     | —        | Obtém access + refresh  |
| POST   | `/api/auth/token/refresh` | —    | Renova access token     |
| GET    | `/api/users/me`       | Bearer   | Perfil do usuário       |

## Estrutura

```
app/
├── apps/
│   ├── core/           # Infraestrutura transversal
│   │   ├── auth.py     # JWTAuth + helpers de token
│   │   ├── exceptions.py  # AppError
│   │   ├── models.py   # BaseModel (uuid, timestamps)
│   │   ├── schemas.py  # Schemas de autenticação
│   │   └── api.py      # Endpoints de auth (/auth/token)
│   └── users/          # Feature: usuários
│       ├── models.py   # User (AbstractUser customizado)
│       ├── schemas.py  # UserOut
│       ├── api.py      # GET /users/me
│       ├── views.py    # Views HTML (hybrid)
│       ├── factories.py
│       └── tests/
├── config/
│   ├── settings.py
│   ├── api.py          # NinjaAPI + exception handlers
│   └── urls.py
└── templates/
```

## Variáveis de ambiente

Veja [`.env.example`](.env.example) para a lista completa.
