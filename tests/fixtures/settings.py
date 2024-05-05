import pytest

from app.settings import Settings


@pytest.fixture
def settings():
    return Settings()
