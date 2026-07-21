import uuid
from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ScheduleInput(BaseModel):
    weekday: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    break_start: time | None = None
    break_end: time | None = None

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.start_time >= self.end_time:
            raise ValueError("O início da jornada deve ser anterior ao fim.")
        if (self.break_start is None) != (self.break_end is None):
            raise ValueError("O intervalo deve possuir início e fim.")
        if self.break_start is not None and not (
            self.start_time < self.break_start < self.break_end < self.end_time
        ):
            raise ValueError("O intervalo deve estar dentro da jornada.")
        return self


class ScheduleResponse(ScheduleInput):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class SpecialtyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    name: str


class BarberCreate(BaseModel):
    user_id: uuid.UUID
    bio: str | None = Field(default=None, max_length=2000)
    specialties: list[str] = Field(default_factory=list, max_length=30)
    schedules: list[ScheduleInput] = Field(default_factory=list, max_length=7)

    @field_validator("specialties")
    @classmethod
    def normalize_specialties(cls, values: list[str]) -> list[str]:
        normalized = list(dict.fromkeys(value.strip() for value in values if value.strip()))
        if any(len(value) > 80 for value in normalized):
            raise ValueError("Cada especialidade deve possuir no máximo 80 caracteres.")
        return normalized

    @field_validator("schedules")
    @classmethod
    def unique_weekdays(cls, values: list[ScheduleInput]) -> list[ScheduleInput]:
        if len({item.weekday for item in values}) != len(values):
            raise ValueError("Não pode haver duas jornadas no mesmo dia da semana.")
        return values


class BarberUpdate(BaseModel):
    bio: str | None = Field(default=None, max_length=2000)
    specialties: list[str] | None = Field(default=None, max_length=30)
    schedules: list[ScheduleInput] | None = Field(default=None, max_length=7)

    @field_validator("specialties")
    @classmethod
    def normalize_specialties(cls, values: list[str] | None) -> list[str] | None:
        if values is None:
            return None
        normalized = list(dict.fromkeys(value.strip() for value in values if value.strip()))
        if any(len(value) > 80 for value in normalized):
            raise ValueError("Cada especialidade deve possuir no máximo 80 caracteres.")
        return normalized

    @field_validator("schedules")
    @classmethod
    def unique_weekdays(cls, values: list[ScheduleInput] | None) -> list[ScheduleInput] | None:
        if values is not None and len({item.weekday for item in values}) != len(values):
            raise ValueError("Não pode haver duas jornadas no mesmo dia da semana.")
        return values


class BarberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    bio: str | None
    active: bool
    specialties: list[SpecialtyResponse]
    schedules: list[ScheduleResponse]
    created_at: datetime
    updated_at: datetime


class UnavailabilityCreate(BaseModel):
    starts_at: datetime
    ends_at: datetime
    reason: str | None = Field(default=None, max_length=240)

    @model_validator(mode="after")
    def validate_range(self):
        if self.starts_at.tzinfo is None or self.ends_at.tzinfo is None:
            raise ValueError("Datas de indisponibilidade devem possuir fuso horário.")
        if self.starts_at >= self.ends_at:
            raise ValueError("O início deve ser anterior ao fim da indisponibilidade.")
        return self


class UnavailabilityResponse(UnavailabilityCreate):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    barber_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
