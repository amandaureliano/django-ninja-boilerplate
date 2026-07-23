from django.contrib.auth import authenticate
from django.http import HttpRequest
from jwt import InvalidTokenError
from ninja import Router

from apps.core.auth import create_access_token, create_refresh_token, decode_token
from apps.core.exceptions import AppError
from apps.core.schemas import TokenObtainIn, TokenObtainOut, TokenRefreshIn, TokenRefreshOut

router = Router(tags=["auth"])


@router.post("/token", response=TokenObtainOut, auth=None)
def obtain_token(request: HttpRequest, payload: TokenObtainIn) -> TokenObtainOut:
    user = authenticate(request, username=payload.username, password=payload.password)
    if not user:
        raise AppError("Credenciais inválidas.", status=401)
    return TokenObtainOut(
        access=create_access_token(user.pk),
        refresh=create_refresh_token(user.pk),
    )


@router.post("/token/refresh", response=TokenRefreshOut, auth=None)
def refresh_token(request: HttpRequest, payload: TokenRefreshIn) -> TokenRefreshOut:
    try:
        data = decode_token(payload.refresh)
        if data.get("type") != "refresh":
            raise AppError("Token inválido.", status=401)
        return TokenRefreshOut(access=create_access_token(data["user_id"]))
    except InvalidTokenError as exc:
        raise AppError("Token inválido ou expirado.", status=401) from exc
