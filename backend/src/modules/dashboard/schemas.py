import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class TopService(BaseModel):
    service_id: uuid.UUID
    name: str
    quantity: int


class TopBarber(BaseModel):
    barber_id: uuid.UUID
    name: str
    revenue: Decimal


class DashboardSummary(BaseModel):
    starts_at: datetime
    ends_at: datetime
    revenue: Decimal
    completed_appointments: int
    new_customers: int
    top_services: list[TopService]
    top_barber: TopBarber | None
