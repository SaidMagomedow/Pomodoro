from dataclasses import dataclass
import pytest
import httpx

from app.settings import Settings
from app.users.auth.schema import GoogleUserData, YandexUserData

import factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from tests.fixtures.users.user_model import EXISTS_GOOGLE_USER_ID, EXISTS_GOOGLE_USER_EMAIL

faker = FakerFactory.create()


@dataclass
class FakeGoogleClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"

@dataclass
class FakeYandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str) -> dict:
        access_token = await self._get_user_access_token(code=code)
        return yandex_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return f"fake_access_token {code}"


@pytest.fixture
def google_client():
    return FakeGoogleClient(settings=Settings(), async_client=httpx.AsyncClient())


@pytest.fixture
def yandex_client():
    return FakeYandexClient(settings=Settings(), async_client=httpx.AsyncClient())


def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=faker.random_int(),
        email=EXISTS_GOOGLE_USER_EMAIL,
        name=faker.name(),
        verified_email=True,
        access_token=faker.sha256()
    )


def yandex_user_info_data() -> dict:
    return YandexUserData(
        id=faker.random_int(),
        default_email=faker.email(),
        login=faker.name(),
        access_token=faker.sha256(),
        real_name=faker.name()
    )