from ninja import Schema


class UserOut(Schema):
    id: int
    username: str
    email: str
