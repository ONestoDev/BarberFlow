from fastapi.testclient import TestClient

from src.main import app
from src.modules.dashboard.routes import admin_only, get_service
from src.modules.dashboard.service import DashboardService
from tests.test_auth_service import make_user
from tests.test_dashboard_service import FakeRepository, period


def test_dashboard_requires_authentication():
    start, end = period()
    response = TestClient(app).get(
        "/api/v1/dashboard/summary",
        params={"starts_at": start.isoformat(), "ends_at": end.isoformat()},
    )
    assert response.status_code == 401


def test_admin_can_read_dashboard():
    start, end = period()
    app.dependency_overrides[get_service] = lambda: DashboardService(FakeRepository())
    app.dependency_overrides[admin_only] = make_user
    try:
        response = TestClient(app).get(
            "/api/v1/dashboard/summary",
            params={"starts_at": start.isoformat(), "ends_at": end.isoformat()},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["revenue"] == "750.00"
    assert response.json()["top_barber"]["name"] == "João"
