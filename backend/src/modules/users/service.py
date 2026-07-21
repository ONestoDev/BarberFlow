from src.modules.users.models import User
from src.modules.users.repository import DuplicateEmailError, UserRepository
from src.modules.users.schemas import UserCreate
from src.shared.security.passwords import hash_password


class EmailAlreadyInUseError(Exception):
    pass


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create(self, data: UserCreate) -> User:
        email = str(data.email).lower()
        if self.repository.get_by_email(email) is not None:
            raise EmailAlreadyInUseError

        user = User(
            name=data.name.strip(),
            email=email,
            password_hash=hash_password(data.password),
            role=data.role,
        )
        try:
            return self.repository.create(user)
        except DuplicateEmailError as exc:
            raise EmailAlreadyInUseError from exc

    def list_active(self) -> list[User]:
        return self.repository.list_active()
