import uuid

import pytest
from fastapi import HTTPException

from src.modules.auth.dependencies import get_current_user, require_roles
from src.shared.database.enums import UserRole
from src.shared.security.tokens import create_access_token
from tests.test_auth_service import make_user


class FakeSession:
    def __init__(self, user):
        self.user = user

    def get(self, model, user_id):
        return self.user


def test_get_current_user_accepts_valid_token():
    user = make_user()
    token = create_access_token(str(user.id))

    assert get_current_user(token=token, db=FakeSession(user)) is user


@pytest.mark.parametrize("token", ["invalid-token", create_access_token("not-a-uuid")])
def test_get_current_user_rejects_invalid_token(token):
    with pytest.raises(HTTPException) as error:
        get_current_user(token=token, db=FakeSession(None))

    assert error.value.status_code == 401


def test_require_roles_rejects_user_without_permission():
    barber = make_user()
    barber.role = UserRole.BARBER

    with pytest.raises(HTTPException) as error:
        require_roles(UserRole.ADMIN)(current_user=barber)

    assert error.value.status_code == 403


def test_require_roles_accepts_admin():
    admin = make_user()

    assert require_roles(UserRole.ADMIN)(current_user=admin) is admin
