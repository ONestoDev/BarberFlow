from fastapi import FastAPI

from src.shared.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API do sistema BarberFlow"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env
    }
