from src.modules.auth.repository import AuthRepository
from src.modules.users.models import User
from src.shared.security.passwords import verify_password
from src.shared.security.tokens import create_access_token


class InvalidCredentialsError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def authenticate(self, email: str, password: str) -> tuple[User, str]:
        user = self.repository.get_user_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError
        if not user.active:
            raise InactiveUserError

        return user, create_access_token(str(user.id))
