import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.modules.users.models import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email.lower())
        return self.db.scalar(statement)

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.get(User, user_id)
