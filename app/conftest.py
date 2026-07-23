import pytest


@pytest.fixture
def user(db):
    from apps.users.factories import UserFactory

    return UserFactory()
