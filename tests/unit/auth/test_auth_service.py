import pytest
import datetime as dt
from app.settings import Settings
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from jose import jwt


pytestmark = pytest.mark.asyncio


async def test_get_google_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_google_redirect_url = settings.google_redirect_url

    mock_auth_service_google_redirect_url = mock_auth_service.get_google_redirect_url()

    assert settings_google_redirect_url == mock_auth_service_google_redirect_url


async def test_get_yandex_redirect_url__success(mock_auth_service: AuthService, settings: Settings):
    settings_yandex_redirect_url = settings.yandex_redirect_url
    mock_auth_service_yandex_redirect_url = mock_auth_service.get_yandex_redirect_url()
    assert settings_yandex_redirect_url == mock_auth_service_yandex_redirect_url


async def test_get_google_redirect_url__fail(mock_auth_service: AuthService):
    settings_google_redirect_url = "https://fake_google_redirect_url.com"
    mock_auth_service_google_redirect_url = mock_auth_service.get_google_redirect_url()
    assert settings_google_redirect_url != mock_auth_service_google_redirect_url


async def test_generate_access_token__success(mock_auth_service: AuthService, settings: Settings):
    user_id = str(1)

    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decoded_access_token = jwt.decode(access_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCODE_ALGORITHM])
    decoded_user_id = decoded_access_token.get("user_id")
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get("expire"), tz=dt.timezone.utc)

    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(days=6)
    assert decoded_user_id == user_id


async def test_get_user_id_from_access_token__success(mock_auth_service: AuthService):
    user_id = str(1)

    access_token = mock_auth_service.generate_access_token(user_id=user_id)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(access_token)

    assert decoded_user_id == user_id


async def test_google_auth__success(mock_auth_service: AuthService):
    code = "fake_code"

    user = await mock_auth_service.google_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)


async def test_yandex_auth__success(mock_auth_service: AuthService):
    code = "fake_code"

    user = await mock_auth_service.yandex_auth(code=code)
    decoded_user_id = mock_auth_service.get_user_id_from_access_token(user.access_token)

    assert user.user_id == decoded_user_id
    assert isinstance(user, UserLoginSchema)
