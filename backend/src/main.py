from fastapi import FastAPI

from src.modules.auth.routes import router as auth_router
from src.modules.appointments.routes import router as appointments_router
from src.modules.barbers.routes import router as barbers_router
from src.modules.customers.routes import router as customers_router
from src.modules.services.routes import category_router, router as services_router
from src.modules.users.routes import router as users_router
from src.shared.config.settings import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="API do sistema BarberFlow"
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(appointments_router, prefix="/api/v1")
app.include_router(barbers_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(category_router, prefix="/api/v1")
app.include_router(services_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env
    }
