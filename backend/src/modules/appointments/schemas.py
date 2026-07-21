import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.shared.database.enums import AppointmentStatus


def aware_datetime(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("A data e hora devem possuir fuso horário.")
    return value


class AppointmentCreate(BaseModel):
    customer_id: uuid.UUID
    barber_id: uuid.UUID
    service_ids: list[uuid.UUID] = Field(min_length=1, max_length=20)
    starts_at: datetime
    notes: str | None = Field(default=None, max_length=2000)

    @field_validator("service_ids")
    @classmethod
    def unique_services(cls, values):
        if len(set(values)) != len(values):
            raise ValueError("Um serviço não pode ser repetido no agendamento.")
        return values

    @field_validator("starts_at")
    @classmethod
    def validate_starts_at(cls, value):
        return aware_datetime(value)


class AppointmentReschedule(BaseModel):
    starts_at: datetime

    @field_validator("starts_at")
    @classmethod
    def validate_starts_at(cls, value):
        return aware_datetime(value)


class AppointmentCancel(BaseModel):
    reason: str = Field(min_length=2, max_length=500)


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AvailableSlot(BaseModel):
    starts_at: datetime
    ends_at: datetime


class AppointmentServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    service_id: uuid.UUID
    service_name_at_time: str
    duration_at_time: int
    price_at_time: Decimal


class AppointmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    customer_id: uuid.UUID
    barber_id: uuid.UUID
    created_by: uuid.UUID
    starts_at: datetime
    ends_at: datetime
    status: AppointmentStatus
    notes: str | None
    cancellation_reason: str | None
    services: list[AppointmentServiceResponse]
    created_at: datetime
    updated_at: datetime
