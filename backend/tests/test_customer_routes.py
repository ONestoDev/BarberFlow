from fastapi.testclient import TestClient

from src.main import app
from src.modules.customers.routes import get_service, staff_only
from tests.test_auth_service import make_user
from tests.test_customer_service import make_customer


class FakeCustomerService:
    def __init__(self):
        self.customer = make_customer()

    def create(self, data):
        return self.customer

    def list(self, query, offset, limit):
        return [self.customer]

    def get(self, customer_id):
        return self.customer

    def update(self, customer_id, data):
        return self.customer

    def deactivate(self, customer_id):
        return self.customer


def test_customers_require_authentication():
    response = TestClient(app).get("/api/v1/customers")

    assert response.status_code == 401


def test_staff_can_create_and_list_customers():
    service = FakeCustomerService()
    app.dependency_overrides[get_service] = lambda: service
    app.dependency_overrides[staff_only] = make_user
    try:
        client = TestClient(app)
        created = client.post(
            "/api/v1/customers",
            json={"name": "Cliente Teste", "phone": "11999998888"},
        )
        listed = client.get("/api/v1/customers?q=Cliente")
    finally:
        app.dependency_overrides.clear()

    assert created.status_code == 201
    assert listed.status_code == 200
    assert listed.json()[0]["phone"] == "11999998888"


def test_staff_can_get_update_and_deactivate_customer():
    service = FakeCustomerService()
    customer_id = service.customer.id
    app.dependency_overrides[get_service] = lambda: service
    app.dependency_overrides[staff_only] = make_user
    try:
        client = TestClient(app)
        fetched = client.get(f"/api/v1/customers/{customer_id}")
        updated = client.patch(
            f"/api/v1/customers/{customer_id}", json={"notes": "Atualizada"}
        )
        deleted = client.delete(f"/api/v1/customers/{customer_id}")
    finally:
        app.dependency_overrides.clear()

    assert fetched.status_code == 200
    assert updated.status_code == 200
    assert deleted.status_code == 204
