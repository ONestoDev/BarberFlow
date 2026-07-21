import uuid
from datetime import datetime, timezone

from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.modules.services.models import Service, ServiceCategory


class DuplicateNameError(Exception):
    pass


class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_category(self, category_id: uuid.UUID) -> ServiceCategory | None:
        return self.db.scalar(select(ServiceCategory).where(ServiceCategory.id == category_id, ServiceCategory.active.is_(True)))

    def get_category_by_name(self, name: str) -> ServiceCategory | None:
        return self.db.scalar(select(ServiceCategory).where(ServiceCategory.name == name))

    def list_categories(self) -> list[ServiceCategory]:
        return list(self.db.scalars(select(ServiceCategory).where(ServiceCategory.active.is_(True)).order_by(ServiceCategory.name)))

    def get_by_id(self, service_id: uuid.UUID) -> Service | None:
        return self.db.scalar(select(Service).where(Service.id == service_id, Service.active.is_(True)))

    def get_by_name(self, name: str) -> Service | None:
        return self.db.scalar(select(Service).where(Service.name == name))

    def list_active(self, query: str | None, category_id: uuid.UUID | None) -> list[Service]:
        statement = select(Service).where(Service.active.is_(True))
        if category_id:
            statement = statement.where(Service.category_id == category_id)
        if query:
            pattern = f"%{query.strip()}%"
            statement = statement.where(or_(Service.name.ilike(pattern), Service.description.ilike(pattern)))
        return list(self.db.scalars(statement.order_by(Service.name)))

    def save(self, entity):
        self.db.add(entity)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise DuplicateNameError from exc
        self.db.refresh(entity)
        return entity

    def deactivate(self, service: Service) -> Service:
        service.active = False
        service.deleted_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(service)
        return service
