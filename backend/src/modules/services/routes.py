import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from src.modules.auth.dependencies import require_roles
from src.modules.services.repository import ServiceRepository
from src.modules.services.schemas import CategoryCreate, CategoryResponse, ServiceCreate, ServiceResponse, ServiceUpdate
from src.modules.services.service import CatalogService, CategoryNotFoundError, NameAlreadyInUseError, ServiceNotFoundError
from src.modules.users.models import User
from src.shared.database.connection import get_db
from src.shared.database.enums import UserRole

router = APIRouter(prefix="/services", tags=["Serviços"])
category_router = APIRouter(prefix="/service-categories", tags=["Categorias de serviço"])
admin_only = require_roles(UserRole.ADMIN)
staff_only = require_roles(UserRole.ADMIN, UserRole.BARBER)


def get_service(db: Session = Depends(get_db)) -> CatalogService:
    return CatalogService(ServiceRepository(db))


def error_response(exc: Exception) -> HTTPException:
    if isinstance(exc, ServiceNotFoundError):
        return HTTPException(status_code=404, detail="Serviço não encontrado.")
    if isinstance(exc, CategoryNotFoundError):
        return HTTPException(status_code=422, detail="Categoria de serviço inválida.")
    return HTTPException(status_code=409, detail="Já existe um registro com este nome.")


@category_router.post("", response_model=CategoryResponse, status_code=201)
def create_category(data: CategoryCreate, service: CatalogService = Depends(get_service), _: User = Depends(admin_only)):
    try:
        return service.create_category(data)
    except NameAlreadyInUseError as exc:
        raise error_response(exc) from exc


@category_router.get("", response_model=list[CategoryResponse])
def list_categories(service: CatalogService = Depends(get_service), _: User = Depends(staff_only)):
    return service.list_categories()


@router.post("", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(data: ServiceCreate, service: CatalogService = Depends(get_service), _: User = Depends(admin_only)):
    try:
        return service.create(data)
    except (CategoryNotFoundError, NameAlreadyInUseError) as exc:
        raise error_response(exc) from exc


@router.get("", response_model=list[ServiceResponse])
def list_services(
    q: str | None = Query(default=None, max_length=160),
    category_id: uuid.UUID | None = None,
    service: CatalogService = Depends(get_service),
    _: User = Depends(staff_only),
):
    return service.list(q, category_id)


@router.get("/{service_id}", response_model=ServiceResponse)
def get_catalog_service(service_id: uuid.UUID, service: CatalogService = Depends(get_service), _: User = Depends(staff_only)):
    try:
        return service.get(service_id)
    except ServiceNotFoundError as exc:
        raise error_response(exc) from exc


@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service(service_id: uuid.UUID, data: ServiceUpdate, service: CatalogService = Depends(get_service), _: User = Depends(admin_only)):
    try:
        return service.update(service_id, data)
    except (ServiceNotFoundError, CategoryNotFoundError, NameAlreadyInUseError) as exc:
        raise error_response(exc) from exc


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_service(service_id: uuid.UUID, service: CatalogService = Depends(get_service), _: User = Depends(admin_only)) -> Response:
    try:
        service.deactivate(service_id)
    except ServiceNotFoundError as exc:
        raise error_response(exc) from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
