import pytest
from ninja.testing import TestClient

from apps.core.auth import create_access_token
from apps.users.api import router

client = TestClient(router)


def test_me_unauthenticated():
    response = client.get("/me")
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_authenticated(user):
    token = create_access_token(user.pk)
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == user.username
