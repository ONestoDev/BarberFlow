from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.main import app
from src.modules.auth.dependencies import get_current_user
from tests.test_auth_service import make_user


def test_me_requires_authentication():
    response = TestClient(app).get("/api/v1/users/me")

    assert response.status_code == 401


def test_me_returns_authenticated_user():
    user = make_user()
    user.created_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    app.dependency_overrides[get_current_user] = lambda: user
    try:
        response = TestClient(app).get("/api/v1/users/me")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["id"] == str(user.id)
    assert response.json()["role"] == "ADMIN"
