from django.http import HttpRequest
from ninja import Router

from apps.core.auth import JWTAuth
from apps.users.schemas import UserOut

router = Router(tags=["users"])


@router.get("/me", response=UserOut, auth=JWTAuth())
def me(request: HttpRequest) -> UserOut:
    return request.auth  # type: ignore[return-value]
