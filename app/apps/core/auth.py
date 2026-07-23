from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja.security import HttpBearer

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)
_ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(tz=UTC) + ACCESS_TOKEN_LIFETIME,
        "type": "access",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=_ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.now(tz=UTC) + REFRESH_TOKEN_LIFETIME,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[_ALGORITHM])


class JWTAuth(HttpBearer):
    def authenticate(self, request: Any, token: str) -> Any:
        try:
            payload = decode_token(token)
            if payload.get("type") != "access":
                return None
            User = get_user_model()
            return User.objects.get(pk=payload["user_id"])
        except Exception:
            return None
