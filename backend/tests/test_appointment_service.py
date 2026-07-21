import uuid
from datetime import datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from src.modules.appointments.models import Appointment
from src.modules.appointments.schemas import (
    AppointmentCancel,
    AppointmentCreate,
    AppointmentReschedule,
    AppointmentStatusUpdate,
)
from src.modules.appointments.service import AppointmentServiceLayer, InvalidAppointmentStateError, OutsideWorkingHoursError, ScheduleConflictError
from src.modules.barbers.models import Barber, BarberSchedule
from src.modules.customers.models import Customer
from src.modules.services.models import Service
from src.shared.database.enums import AppointmentStatus

LOCAL = ZoneInfo("America/Sao_Paulo")


class FakeRepository:
    def __init__(self):
        self.customer = Customer(id=uuid.uuid4(), active=True)
        self.barber = Barber(
            id=uuid.uuid4(), user_id=uuid.uuid4(), active=True,
            schedules=[BarberSchedule(weekday=0, start_time=time(8), end_time=time(18), break_start=time(12), break_end=time(13))],
        )
        self.services = [
            Service(id=uuid.uuid4(), name="Corte", duration_minutes=30, price=Decimal("40.00"), active=True),
            Service(id=uuid.uuid4(), name="Barba", duration_minutes=20, price=Decimal("25.00"), active=True),
        ]
        self.appointment = None
        self.conflict = False
        self.unavailable = False

    def get_customer(self, customer_id): return self.customer
    def get_barber(self, barber_id): return self.barber
    def get_services(self, service_ids): return self.services
    def get(self, appointment_id): return self.appointment
    def list(self, starts_at, ends_at, barber_id): return [self.appointment] if self.appointment else []
    def has_conflict(self, *args): return self.conflict
    def has_unavailability(self, *args): return self.unavailable
    def save(self, appointment): self.appointment = appointment; return appointment


def monday(hour=9, minute=0):
    return datetime(2026, 7, 27, hour, minute, tzinfo=LOCAL)


def payload(repository, starts_at=None):
    return AppointmentCreate(
        customer_id=repository.customer.id,
        barber_id=repository.barber.id,
        service_ids=[item.id for item in repository.services],
        starts_at=starts_at or monday(),
    )


def test_create_calculates_duration_and_historical_snapshots():
    repository = FakeRepository()
    result = AppointmentServiceLayer(repository).create(payload(repository), uuid.uuid4())
    assert result.ends_at - result.starts_at == timedelta(minutes=50)
    assert [item.price_at_time for item in result.services] == [Decimal("40.00"), Decimal("25.00")]
    assert result.status == AppointmentStatus.SCHEDULED


def test_create_rejects_lunch_break():
    repository = FakeRepository()
    with pytest.raises(OutsideWorkingHoursError):
        AppointmentServiceLayer(repository).create(payload(repository, monday(11, 30)), uuid.uuid4())


@pytest.mark.parametrize("attribute", ["conflict", "unavailable"])
def test_create_rejects_conflicts(attribute):
    repository = FakeRepository()
    setattr(repository, attribute, True)
    with pytest.raises(ScheduleConflictError):
        AppointmentServiceLayer(repository).create(payload(repository), uuid.uuid4())


def test_cancel_releases_appointment_with_reason():
    repository = FakeRepository()
    service = AppointmentServiceLayer(repository)
    appointment = service.create(payload(repository), uuid.uuid4())
    result = service.cancel(appointment.id, AppointmentCancel(reason="Cliente desistiu"))
    assert result.status == AppointmentStatus.CANCELED
    assert result.cancellation_reason == "Cliente desistiu"


def test_completed_appointment_cannot_be_rescheduled():
    repository = FakeRepository()
    appointment = Appointment(
        id=uuid.uuid4(), barber_id=repository.barber.id,
        starts_at=monday(), ends_at=monday() + timedelta(minutes=30),
        status=AppointmentStatus.COMPLETED,
    )
    repository.appointment = appointment
    with pytest.raises(InvalidAppointmentStateError):
        AppointmentServiceLayer(repository).reschedule(appointment.id, AppointmentReschedule(starts_at=monday(10)))


def test_reschedule_preserves_duration():
    repository = FakeRepository()
    service = AppointmentServiceLayer(repository)
    appointment = service.create(payload(repository), uuid.uuid4())
    result = service.reschedule(appointment.id, AppointmentReschedule(starts_at=monday(10)))
    assert result.starts_at.astimezone(LOCAL).hour == 10
    assert result.ends_at - result.starts_at == timedelta(minutes=50)


def test_valid_state_machine_reaches_completed():
    repository = FakeRepository()
    service = AppointmentServiceLayer(repository)
    appointment = service.create(payload(repository), uuid.uuid4())

    for target in (
        AppointmentStatus.CONFIRMED,
        AppointmentStatus.IN_PROGRESS,
        AppointmentStatus.COMPLETED,
    ):
        service.change_status(appointment.id, AppointmentStatusUpdate(status=target))

    assert appointment.status == AppointmentStatus.COMPLETED


def test_state_machine_rejects_skipped_state():
    repository = FakeRepository()
    service = AppointmentServiceLayer(repository)
    appointment = service.create(payload(repository), uuid.uuid4())

    with pytest.raises(InvalidAppointmentStateError):
        service.change_status(
            appointment.id,
            AppointmentStatusUpdate(status=AppointmentStatus.COMPLETED),
        )


def test_available_slots_respect_workday_lunch_and_duration():
    repository = FakeRepository()

    slots = AppointmentServiceLayer(repository).available_slots(
        repository.barber.id,
        monday().date(),
        [item.id for item in repository.services],
    )

    assert len(slots) == 30
    assert slots[0].starts_at.hour == 8
    assert all(not (slot.starts_at.hour == 12) for slot in slots)
    assert all(slot.ends_at - slot.starts_at == timedelta(minutes=50) for slot in slots)


def test_available_slots_returns_empty_on_day_off():
    repository = FakeRepository()

    slots = AppointmentServiceLayer(repository).available_slots(
        repository.barber.id,
        monday().date() + timedelta(days=1),
        [item.id for item in repository.services],
    )

    assert slots == []
