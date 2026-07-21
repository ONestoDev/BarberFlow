import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


def normalize_name(value: str) -> str:
    value = " ".join(value.split())
    if len(value) < 2:
        raise ValueError("O nome deve possuir pelo menos 2 caracteres.")
    return value


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return normalize_name(value)


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str
    active: bool
    created_at: datetime
    updated_at: datetime


class ServiceCreate(BaseModel):
    category_id: uuid.UUID
    name: str = Field(min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    duration_minutes: int = Field(gt=0, le=1440)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return normalize_name(value)


class ServiceUpdate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = Field(default=None, max_length=2000)
    duration_minutes: int | None = Field(default=None, gt=0, le=1440)
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        return normalize_name(value) if value is not None else None


class ServiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    category_id: uuid.UUID
    name: str
    description: str | None
    duration_minutes: int
    price: Decimal
    active: bool
    created_at: datetime
    updated_at: datetime
