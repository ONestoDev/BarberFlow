import uuid

import pytest

from src.modules.auth.service import (
    AuthService,
    InactiveUserError,
    InvalidCredentialsError,
)
from src.modules.users.models import User
from src.shared.database.enums import UserRole
from src.shared.security.passwords import hash_password


class FakeAuthRepository:
    def __init__(self, user: User | None):
        self.user = user

    def get_user_by_email(self, email: str) -> User | None:
        return self.user


def make_user(*, active: bool = True) -> User:
    return User(
        id=uuid.uuid4(),
        name="Administrador",
        email="admin@example.com",
        password_hash=hash_password("senha-segura"),
        role=UserRole.ADMIN,
        active=active,
    )


def test_authenticate_returns_token_for_valid_credentials():
    user, token = AuthService(FakeAuthRepository(make_user())).authenticate(
        "admin@example.com", "senha-segura"
    )

    assert user.email == "admin@example.com"
    assert token


def test_authenticate_rejects_invalid_credentials():
    with pytest.raises(InvalidCredentialsError):
        AuthService(FakeAuthRepository(None)).authenticate(
            "inexistente@example.com", "senha"
        )


def test_authenticate_rejects_inactive_user():
    with pytest.raises(InactiveUserError):
        AuthService(FakeAuthRepository(make_user(active=False))).authenticate(
            "admin@example.com", "senha-segura"
        )
