from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "BarberFlow"
    app_env: str = "development"
    app_timezone: str = "America/Sao_Paulo"
    appointment_slot_interval_minutes: int = Field(default=15, gt=0, le=120)

    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_in_minutes: int = 60

    @field_validator("database_url")
    @classmethod
    def use_psycopg_v3_driver(cls, value: str) -> str:
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+psycopg://", 1)
        return value


settings = Settings()
