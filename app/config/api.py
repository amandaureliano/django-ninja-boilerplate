from django.http import Http404, HttpRequest
from ninja import NinjaAPI

from apps.core.api import router as auth_router
from apps.core.exceptions import AppError
from apps.users.api import router as users_router

api = NinjaAPI(title="API", version="1.0.0", docs_url="/docs")


@api.exception_handler(Http404)
def not_found(request: HttpRequest, exc: Http404):
    return api.create_response(request, {"detail": "Não encontrado."}, status=404)


@api.exception_handler(AppError)
def app_error(request: HttpRequest, exc: AppError):
    return api.create_response(request, {"detail": exc.message}, status=exc.status)


@api.get("/health", tags=["system"])
def health(request: HttpRequest):
    return {"status": "ok"}


api.add_router("/auth", auth_router)
api.add_router("/users", users_router)
