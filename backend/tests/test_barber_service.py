import uuid
from datetime import datetime, time, timedelta, timezone

import pytest
from pydantic import ValidationError

from src.modules.barbers.models import Barber
from src.modules.barbers.schemas import BarberCreate, BarberUpdate, ScheduleInput, UnavailabilityCreate
from src.modules.barbers.service import (
    BarberNotFoundError,
    BarberService,
    InvalidBarberUserError,
    UserAlreadyLinkedError,
)
from src.shared.database.enums import UserRole
from tests.test_auth_service import make_user


class FakeBarberRepository:
    def __init__(self, user=None, barber=None, linked=None):
        self.user = user
        self.barber = barber
        self.linked = linked
        self.unavailabilities = []

    def get_user(self, user_id):
        return self.user

    def get_by_user_id(self, user_id):
        return self.linked

    def get_by_id(self, barber_id):
        return self.barber

    def list_active(self):
        return [self.barber] if self.barber else []

    def save(self, barber):
        self.barber = barber
        return barber

    def add_unavailability(self, item):
        self.unavailabilities.append(item)
        return item

    def list_unavailabilities(self, barber_id):
        return self.unavailabilities


def barber_user():
    user = make_user()
    user.role = UserRole.BARBER
    return user


def barber_data(user_id):
    return BarberCreate(
        user_id=user_id,
        specialties=["Corte", "Corte", " Barba "],
        schedules=[
            ScheduleInput(
                weekday=0,
                start_time=time(8),
                end_time=time(18),
                break_start=time(12),
                break_end=time(13),
            )
        ],
    )


def test_create_barber_links_valid_user_and_details():
    user = barber_user()

    barber = BarberService(FakeBarberRepository(user=user)).create(barber_data(user.id))

    assert barber.user_id == user.id
    assert [item.name for item in barber.specialties] == ["Corte", "Barba"]
    assert barber.schedules[0].weekday == 0


def test_create_barber_rejects_non_barber_user():
    user = make_user()
    with pytest.raises(InvalidBarberUserError):
        BarberService(FakeBarberRepository(user=user)).create(barber_data(user.id))


def test_create_barber_rejects_already_linked_user():
    user = barber_user()
    with pytest.raises(UserAlreadyLinkedError):
        BarberService(FakeBarberRepository(user=user, linked=object())).create(barber_data(user.id))


def test_get_barber_rejects_unknown_id():
    with pytest.raises(BarberNotFoundError):
        BarberService(FakeBarberRepository()).get(uuid.uuid4())


def test_update_replaces_specialties():
    barber = Barber(id=uuid.uuid4(), user_id=uuid.uuid4(), active=True)
    repository = FakeBarberRepository(barber=barber)

    updated = BarberService(repository).update(
        barber.id, BarberUpdate(bio="Especialista", specialties=["Navalha"])
    )

    assert updated.bio == "Especialista"
    assert [item.name for item in updated.specialties] == ["Navalha"]


def test_add_and_list_unavailability():
    barber = Barber(id=uuid.uuid4(), user_id=uuid.uuid4(), active=True)
    repository = FakeBarberRepository(barber=barber)
    service = BarberService(repository)
    start = datetime.now(timezone.utc)
    data = UnavailabilityCreate(starts_at=start, ends_at=start + timedelta(days=2), reason="Férias")

    created = service.add_unavailability(barber.id, data)

    assert created.reason == "Férias"
    assert service.list_unavailabilities(barber.id) == [created]


def test_schedule_rejects_invalid_break():
    with pytest.raises(ValidationError):
        ScheduleInput(
            weekday=1,
            start_time=time(8),
            end_time=time(18),
            break_start=time(12),
        )


def test_unavailability_requires_timezone():
    with pytest.raises(ValidationError):
        UnavailabilityCreate(
            starts_at=datetime(2026, 8, 1),
            ends_at=datetime(2026, 8, 2),
        )
