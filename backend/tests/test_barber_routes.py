import uuid
from datetime import datetime, time, timedelta, timezone

from fastapi.testclient import TestClient

from src.main import app
from src.modules.barbers.models import Barber, BarberSchedule, BarberSpecialty, BarberUnavailability
from src.modules.barbers.routes import admin_only, get_service, staff_only
from tests.test_auth_service import make_user


def make_barber():
    now = datetime.now(timezone.utc)
    return Barber(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        bio=None,
        active=True,
        created_at=now,
        updated_at=now,
        specialties=[BarberSpecialty(id=uuid.uuid4(), name="Corte")],
        schedules=[
            BarberSchedule(
                id=uuid.uuid4(), weekday=0, start_time=time(8), end_time=time(18)
            )
        ],
    )


class FakeBarberService:
    def __init__(self):
        self.barber = make_barber()
        now = datetime.now(timezone.utc)
        self.unavailability = BarberUnavailability(
            id=uuid.uuid4(),
            barber_id=self.barber.id,
            starts_at=now,
            ends_at=now + timedelta(days=1),
            reason="Folga",
            created_at=now,
            updated_at=now,
        )

    def create(self, data): return self.barber
    def list(self): return [self.barber]
    def get(self, barber_id): return self.barber
    def update(self, barber_id, data): return self.barber
    def add_unavailability(self, barber_id, data): return self.unavailability
    def list_unavailabilities(self, barber_id): return [self.unavailability]


def test_barbers_require_authentication():
    assert TestClient(app).get("/api/v1/barbers").status_code == 401


def test_barber_crud_routes():
    service = FakeBarberService()
    app.dependency_overrides[get_service] = lambda: service
    app.dependency_overrides[admin_only] = make_user
    app.dependency_overrides[staff_only] = make_user
    try:
        client = TestClient(app)
        created = client.post("/api/v1/barbers", json={"user_id": str(uuid.uuid4())})
        listed = client.get("/api/v1/barbers")
        fetched = client.get(f"/api/v1/barbers/{service.barber.id}")
        updated = client.patch(f"/api/v1/barbers/{service.barber.id}", json={"bio": "Bio"})
    finally:
        app.dependency_overrides.clear()

    assert [created.status_code, listed.status_code, fetched.status_code, updated.status_code] == [201, 200, 200, 200]


def test_unavailability_routes():
    service = FakeBarberService()
    app.dependency_overrides[get_service] = lambda: service
    app.dependency_overrides[admin_only] = make_user
    app.dependency_overrides[staff_only] = make_user
    payload = {
        "starts_at": service.unavailability.starts_at.isoformat(),
        "ends_at": service.unavailability.ends_at.isoformat(),
        "reason": "Folga",
    }
    try:
        client = TestClient(app)
        created = client.post(
            f"/api/v1/barbers/{service.barber.id}/unavailabilities", json=payload
        )
        listed = client.get(f"/api/v1/barbers/{service.barber.id}/unavailabilities")
    finally:
        app.dependency_overrides.clear()

    assert created.status_code == 201
    assert listed.status_code == 200
