import uuid

from src.modules.services.models import Service, ServiceCategory
from src.modules.services.repository import DuplicateNameError, ServiceRepository
from src.modules.services.schemas import CategoryCreate, ServiceCreate, ServiceUpdate


class CategoryNotFoundError(Exception): pass
class ServiceNotFoundError(Exception): pass
class NameAlreadyInUseError(Exception): pass


class CatalogService:
    def __init__(self, repository: ServiceRepository):
        self.repository = repository

    def create_category(self, data: CategoryCreate) -> ServiceCategory:
        if self.repository.get_category_by_name(data.name) is not None:
            raise NameAlreadyInUseError
        return self._save(ServiceCategory(name=data.name))

    def list_categories(self) -> list[ServiceCategory]:
        return self.repository.list_categories()

    def create(self, data: ServiceCreate) -> Service:
        self._require_category(data.category_id)
        if self.repository.get_by_name(data.name) is not None:
            raise NameAlreadyInUseError
        return self._save(Service(**data.model_dump()))

    def get(self, service_id: uuid.UUID) -> Service:
        service = self.repository.get_by_id(service_id)
        if service is None:
            raise ServiceNotFoundError
        return service

    def list(self, query: str | None, category_id: uuid.UUID | None) -> list[Service]:
        return self.repository.list_active(query, category_id)

    def update(self, service_id: uuid.UUID, data: ServiceUpdate) -> Service:
        service = self.get(service_id)
        changes = data.model_dump(exclude_unset=True)
        if changes.get("category_id") is not None:
            self._require_category(changes["category_id"])
        new_name = changes.get("name")
        if new_name and new_name != service.name and self.repository.get_by_name(new_name):
            raise NameAlreadyInUseError
        for field, value in changes.items():
            if field != "description" and value is None:
                continue
            setattr(service, field, value)
        return self._save(service)

    def deactivate(self, service_id: uuid.UUID) -> Service:
        return self.repository.deactivate(self.get(service_id))

    def _require_category(self, category_id: uuid.UUID) -> ServiceCategory:
        category = self.repository.get_category(category_id)
        if category is None:
            raise CategoryNotFoundError
        return category

    def _save(self, entity):
        try:
            return self.repository.save(entity)
        except DuplicateNameError as exc:
            raise NameAlreadyInUseError from exc
