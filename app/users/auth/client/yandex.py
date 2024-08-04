from dataclasses import dataclass
import httpx

from app.users.auth.schema import YandexUserData
from app.settings import Settings


@dataclass
class YandexClient:
    settings: Settings
    async_client: httpx.AsyncClient

    async def get_user_info(self, code: str):
        access_token = await self._get_user_access_token(code=code)
        async with self.async_client as client:
            user_info = await client.get(
                "https://login.yandex.ru/info?format=json", headers={"Authorization": f"OAuth {access_token}"}
            )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_user_access_token(self, code: str) -> str:
        async with self.async_client as client:
            response = await client.post(
                self.settings.YANDEX_TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": self.settings.YANDEX_CLIENT_ID,
                    "client_secret": self.settings.YANDEX_SECRET_KEY,
                },
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            )
        return response.json()["access_token"]
