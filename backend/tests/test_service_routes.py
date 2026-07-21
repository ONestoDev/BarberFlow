import uuid
from datetime import datetime, timezone
from decimal import Decimal

from fastapi.testclient import TestClient

from src.main import app
from src.modules.services.models import Service, ServiceCategory
from src.modules.services.routes import admin_only, get_service, staff_only
from tests.test_auth_service import make_user


class FakeCatalog:
    def __init__(self):
        now = datetime.now(timezone.utc)
        self.category = ServiceCategory(id=uuid.uuid4(), name="Cabelo", active=True, created_at=now, updated_at=now)
        self.item = Service(id=uuid.uuid4(), category_id=self.category.id, name="Corte", description=None, duration_minutes=30, price=Decimal("40.00"), active=True, created_at=now, updated_at=now)
    def create_category(self, data): return self.category
    def list_categories(self): return [self.category]
    def create(self, data): return self.item
    def list(self, query, category_id): return [self.item]
    def get(self, service_id): return self.item
    def update(self, service_id, data): return self.item
    def deactivate(self, service_id): return self.item


def test_catalog_requires_authentication():
    assert TestClient(app).get("/api/v1/services").status_code == 401


def test_category_and_service_routes():
    catalog = FakeCatalog()
    app.dependency_overrides[get_service] = lambda: catalog
    app.dependency_overrides[admin_only] = make_user
    app.dependency_overrides[staff_only] = make_user
    try:
        client = TestClient(app)
        responses = [
            client.post("/api/v1/service-categories", json={"name": "Cabelo"}),
            client.get("/api/v1/service-categories"),
            client.post("/api/v1/services", json={"category_id": str(catalog.category.id), "name": "Corte", "duration_minutes": 30, "price": "40.00"}),
            client.get("/api/v1/services"),
            client.get(f"/api/v1/services/{catalog.item.id}"),
            client.patch(f"/api/v1/services/{catalog.item.id}", json={"price": "45.00"}),
            client.delete(f"/api/v1/services/{catalog.item.id}"),
        ]
    finally:
        app.dependency_overrides.clear()
    assert [response.status_code for response in responses] == [201, 200, 201, 200, 200, 200, 204]
