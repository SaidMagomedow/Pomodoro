from sqlalchemy import insert, select
from sqlalchemy.orm import Session

from dataclasses import dataclass
from models import UserProfile
from schema import UserCreateSchema


@dataclass
class UserRepository:
    db_session: Session

    def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = insert(UserProfile).values(
            **user.model_dump(),
        ).returning(UserProfile.id)

        with self.db_session() as session:
            user_id: int = session.execute(query).scalar()
            session.commit()
            session.flush()
            return self.get_user(user_id)

    def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()

    def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        with self.db_session() as session:
            return session.execute(query).scalar_one_or_none()
