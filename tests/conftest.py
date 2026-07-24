import pytest


@pytest.fixture
def user(db):
    from factories import UserFactory

    return UserFactory()
