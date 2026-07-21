from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.modules.users.models import User
from src.shared.database.enums import UserRole


class DuplicateEmailError(Exception):
    pass


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.lower()))

    def list_active(self) -> list[User]:
        statement = select(User).where(User.active.is_(True)).order_by(User.name)
        return list(self.db.scalars(statement))

    def has_admin(self) -> bool:
        statement = select(User.id).where(User.role == UserRole.ADMIN).limit(1)
        return self.db.scalar(statement) is not None

    def create(self, user: User) -> User:
        self.db.add(user)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicateEmailError from exc
        self.db.refresh(user)
        return user
