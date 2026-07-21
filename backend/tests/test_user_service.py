import pytest

from src.modules.users.repository import DuplicateEmailError
from src.modules.users.schemas import UserCreate
from src.modules.users.service import EmailAlreadyInUseError, UserService
from src.shared.database.enums import UserRole
from src.shared.security.passwords import verify_password


class FakeUserRepository:
    def __init__(self, existing_user=None, duplicate_on_create=False):
        self.existing_user = existing_user
        self.duplicate_on_create = duplicate_on_create
        self.created_user = None

    def get_by_email(self, email):
        return self.existing_user

    def create(self, user):
        if self.duplicate_on_create:
            raise DuplicateEmailError
        self.created_user = user
        return user

    def list_active(self):
        return []


def user_data():
    return UserCreate(
        name=" Novo Administrador ",
        email="NOVO@example.com",
        password="senha-segura",
        role=UserRole.ADMIN,
    )


def test_create_user_normalizes_data_and_hashes_password():
    repository = FakeUserRepository()

    user = UserService(repository).create(user_data())

    assert user.name == "Novo Administrador"
    assert user.email == "novo@example.com"
    assert user.password_hash != "senha-segura"
    assert verify_password("senha-segura", user.password_hash)


def test_create_user_rejects_existing_email():
    with pytest.raises(EmailAlreadyInUseError):
        UserService(FakeUserRepository(existing_user=object())).create(user_data())


def test_create_user_handles_database_uniqueness_race():
    with pytest.raises(EmailAlreadyInUseError):
        UserService(FakeUserRepository(duplicate_on_create=True)).create(user_data())
