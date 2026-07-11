from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    app_name: str = "BarberFlow"
    app_env: str = "development"

    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_in_minutes: int = 60


settings = Settings()
