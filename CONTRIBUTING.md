# Guia de contribuição

## Criando um novo app

```bash
mkdir -p app/apps/nome_do_app/tests
uv run python app/manage.py startapp nome_do_app app/apps/nome_do_app
```

Registre em `INSTALLED_APPS` no [settings.py](app/config/settings.py):

```python
"apps.nome_do_app",
```

### Estrutura padrão de um app

```
apps/nome_do_app/
├── models.py
├── schemas.py
├── api.py
├── views.py       # apenas se precisar de páginas HTML
├── urls.py        # apenas se precisar de páginas HTML
├── admin.py
├── factories.py
├── apps.py
└── tests/
    └── test_api.py
```

## Convenções

### Models

Herde `BaseModel` para obter `id` (UUID), `created_at` e `updated_at` automáticos:

```python
from apps.core.models import BaseModel

class Produto(BaseModel):
    nome = models.CharField(max_length=200)
```

No admin, herde `BaseAdmin` para tornar os campos de auditoria somente leitura:

```python
from apps.core.admin import BaseAdmin

@admin.register(Produto)
class ProdutoAdmin(BaseAdmin):
    list_display = ("nome", "created_at")
```

### Endpoints (API)

Cada app expõe um `Router`. Registre-o em [`config/api.py`](app/config/api.py):

```python
from apps.nome_do_app.api import router as nome_router
api.add_router("/nome", nome_router)
```

Use `auth=JWTAuth()` para proteger endpoints:

```python
from apps.core.auth import JWTAuth

@router.get("/", response=ItemOut, auth=JWTAuth())
def listar(request: HttpRequest) -> list[ItemOut]:
    ...
```

### Erros de domínio

Use `AppError` para erros esperados — ela vira JSON automaticamente:

```python
from apps.core.exceptions import AppError

raise AppError("Produto não encontrado.", status=404)
# → {"detail": "Produto não encontrado."} HTTP 404
```

### Schemas

Schemas de entrada e saída ficam em `schemas.py` do app:

```python
from ninja import Schema

class ItemIn(Schema):
    nome: str
    preco: float

class ItemOut(Schema):
    id: str   # UUID como string
    nome: str
    preco: float
```

### Testes

Use `UserFactory` (e crie factories similares para seus models):

```python
# factories.py
import factory
from apps.nome_do_app.models import Produto

class ProdutoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Produto

    nome = factory.Sequence(lambda n: f"Produto {n}")
```

Marque testes que acessam banco com `@pytest.mark.django_db`:

```python
@pytest.mark.django_db
def test_criar_produto():
    produto = ProdutoFactory()
    assert produto.id is not None
```

Use `TestClient` do Ninja para testar endpoints diretamente:

```python
from ninja.testing import TestClient
from apps.nome_do_app.api import router

client = TestClient(router)

@pytest.mark.django_db
def test_listar(user):
    token = create_access_token(user.pk)
    response = client.get("/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
```

## Qualidade de código

O pre-commit roda automaticamente antes de cada commit:

```bash
uv run pre-commit install   # instalar hooks (uma vez)
uv run pre-commit run --all-files  # rodar manualmente
```

Hooks ativos: `ruff` (lint + format) e `mypy` (tipos).
