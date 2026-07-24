import requests
from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest
from jwt import InvalidTokenError
from ninja import Router

from apps.core.auth import create_access_token, create_refresh_token, decode_token
from apps.core.exceptions import AppError
from apps.core.schemas import (
    GoogleTokenIn,
    TokenObtainIn,
    TokenObtainOut,
    TokenRefreshIn,
    TokenRefreshOut,
)

User = get_user_model()

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


@router.post("/social/google", response=TokenObtainOut, auth=None)
def google_auth(request: HttpRequest, payload: GoogleTokenIn) -> TokenObtainOut:
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {payload.access_token}"},
        timeout=10,
    )
    if resp.status_code != 200:
        raise AppError("Token Google inválido.", status=401)

    data = resp.json()
    email: str = data.get("email", "")
    if not email or not data.get("email_verified"):
        raise AppError("Email Google não verificado.", status=400)

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={
            "username": email[:150],
            "first_name": data.get("given_name", ""),
            "last_name": data.get("family_name", ""),
        },
    )
    return TokenObtainOut(
        access=create_access_token(user.pk),
        refresh=create_refresh_token(user.pk),
    )
