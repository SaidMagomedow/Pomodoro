from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from dataclasses import dataclass
from models import UserProfile


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session() as session:
            return await session.execute(query).scalar_one_or_none()

    async def create_user(self, username: str, password: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=username,
            password=password,
        ).returning(UserProfile.id)
        async with self.db_session() as session:
            user_id: int = await session.execute(query).scalar()
            await session.commit()
            await session.flush()
            return self.get_user(user_id)

    async def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session() as session:
            return await session.execute(query).scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session() as session:
            return await session.execute(query).scalar_one_or_none()
