from ninja import Schema


class TokenObtainIn(Schema):
    username: str
    password: str


class TokenObtainOut(Schema):
    access: str
    refresh: str


class TokenRefreshIn(Schema):
    refresh: str


class TokenRefreshOut(Schema):
    access: str


class GoogleTokenIn(Schema):
    access_token: str
