import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from src.modules.dashboard.service import DashboardService


class FakeRepository:
    def __init__(self, empty=False):
        self.service_id = uuid.uuid4()
        self.barber_id = uuid.uuid4()
        self.empty = empty

    def revenue(self, starts_at, ends_at):
        return Decimal("750.00") if not self.empty else Decimal("0.00")

    def completed_appointments(self, starts_at, ends_at):
        return 12 if not self.empty else 0

    def new_customers(self, starts_at, ends_at):
        return 4 if not self.empty else 0

    def top_services(self, starts_at, ends_at):
        return [] if self.empty else [(self.service_id, "Corte", 8)]

    def top_barber(self, starts_at, ends_at):
        return None if self.empty else (self.barber_id, "João", Decimal("500.00"))


def period():
    start = datetime(2026, 7, 1, tzinfo=timezone.utc)
    return start, start + timedelta(days=31)


def test_dashboard_builds_business_indicators():
    repository = FakeRepository()
    result = DashboardService(repository).summary(*period())

    assert result.revenue == Decimal("750.00")
    assert result.completed_appointments == 12
    assert result.new_customers == 4
    assert result.top_services[0].quantity == 8
    assert result.top_barber.barber_id == repository.barber_id
    assert result.top_barber.revenue == Decimal("500.00")


def test_dashboard_returns_zeroes_without_movement():
    result = DashboardService(FakeRepository(empty=True)).summary(*period())

    assert result.revenue == Decimal("0.00")
    assert result.completed_appointments == 0
    assert result.top_services == []
    assert result.top_barber is None


def test_dashboard_rejects_invalid_period():
    start, _ = period()
    with pytest.raises(ValueError):
        DashboardService(FakeRepository()).summary(start, start)
