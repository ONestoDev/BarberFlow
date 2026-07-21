import uuid
from decimal import Decimal

import pytest

from src.modules.services.models import Service, ServiceCategory
from src.modules.services.repository import DuplicateNameError
from src.modules.services.schemas import CategoryCreate, ServiceCreate, ServiceUpdate
from src.modules.services.service import CatalogService, CategoryNotFoundError, NameAlreadyInUseError, ServiceNotFoundError


class FakeRepository:
    def __init__(self, category=None, service=None, duplicate=False):
        self.category = category
        self.service = service
        self.duplicate = duplicate

    def get_category(self, category_id): return self.category
    def get_category_by_name(self, name): return self.category if self.duplicate else None
    def list_categories(self): return [self.category] if self.category else []
    def get_by_id(self, service_id): return self.service
    def get_by_name(self, name): return self.service if self.duplicate else None
    def list_active(self, query, category_id): return [self.service] if self.service else []
    def save(self, entity):
        if self.duplicate: raise DuplicateNameError
        return entity
    def deactivate(self, service):
        service.active = False
        return service


def category(): return ServiceCategory(id=uuid.uuid4(), name="Cabelo", active=True)


def service_data(category_id):
    return ServiceCreate(category_id=category_id, name=" Corte Masculino ", duration_minutes=30, price=Decimal("45.90"))


def test_create_category_normalizes_name():
    result = CatalogService(FakeRepository()).create_category(CategoryCreate(name="  Cabelo   e Barba "))
    assert result.name == "Cabelo e Barba"


def test_create_service_uses_decimal_price():
    item_category = category()
    result = CatalogService(FakeRepository(category=item_category)).create(service_data(item_category.id))
    assert result.name == "Corte Masculino"
    assert result.price == Decimal("45.90")


def test_create_service_requires_active_category():
    with pytest.raises(CategoryNotFoundError):
        CatalogService(FakeRepository()).create(service_data(uuid.uuid4()))


def test_duplicate_name_is_rejected():
    with pytest.raises(NameAlreadyInUseError):
        CatalogService(FakeRepository(duplicate=True)).create_category(CategoryCreate(name="Cabelo"))


def test_get_unknown_service_is_rejected():
    with pytest.raises(ServiceNotFoundError):
        CatalogService(FakeRepository()).get(uuid.uuid4())


def test_update_and_deactivate_service():
    item_category = category()
    item = Service(id=uuid.uuid4(), category_id=item_category.id, name="Corte", duration_minutes=30, price=Decimal("40"), active=True)
    catalog = CatalogService(FakeRepository(category=item_category, service=item))
    updated = catalog.update(item.id, ServiceUpdate(price=Decimal("50.00"), description="Novo"))
    assert updated.price == Decimal("50.00")
    assert catalog.deactivate(item.id).active is False
