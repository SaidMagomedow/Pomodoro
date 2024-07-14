import pytest
import pytest_asyncio

from app.dependecy import get_broker_producer, get_broker_consumer
from app.settings import Settings
from app.users.auth.client import MailClient
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest_asyncio.fixture
async def mock_auth_service(yandex_client, google_client, fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(
            settings=Settings(),
            broker_producer=await get_broker_producer(),
        )
    )


@pytest_asyncio.fixture
async def auth_service(yandex_client, google_client, mock_auth_service, get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        mail_client=MailClient(
            settings=Settings(),
            broker_producer=await get_broker_producer(),
        )
    )
