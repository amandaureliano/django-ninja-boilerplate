import pytest
from factories import UserFactory
from ninja.testing import TestClient

from apps.core.auth import create_refresh_token
from config.api import api

client = TestClient(api)


@pytest.mark.django_db
def test_obtain_token():
    user = UserFactory()
    response = client.post(
        "/auth/token", json={"username": user.username, "password": "testpass123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access" in data
    assert "refresh" in data


@pytest.mark.django_db
def test_obtain_token_invalid_credentials():
    response = client.post(
        "/auth/token", json={"username": "wrong", "password": "wrong"}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_refresh_token(user):
    refresh = create_refresh_token(user.pk)
    response = client.post("/auth/token/refresh", json={"refresh": refresh})
    assert response.status_code == 200
    assert "access" in response.json()
