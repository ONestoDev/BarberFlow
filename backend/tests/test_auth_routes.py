from fastapi.testclient import TestClient

from src.main import app
from src.shared.database.connection import get_db
from tests.test_auth_service import make_user


class FakeSession:
    def __init__(self, user):
        self.user = user

    def scalar(self, statement):
        return self.user


def test_login_returns_bearer_token():
    def override_get_db():
        yield FakeSession(make_user())

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = TestClient(app).post(
            "/api/v1/auth/login",
            data={"username": "admin@example.com", "password": "senha-segura"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_rejects_invalid_credentials():
    def override_get_db():
        yield FakeSession(None)

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = TestClient(app).post(
            "/api/v1/auth/login",
            data={"username": "unknown@example.com", "password": "senha-incorreta"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuário ou senha inválidos."


def test_login_rejects_inactive_user():
    def override_get_db():
        yield FakeSession(make_user(active=False))

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = TestClient(app).post(
            "/api/v1/auth/login",
            data={"username": "admin@example.com", "password": "senha-segura"},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert response.json()["detail"] == "Sua conta está desativada."
