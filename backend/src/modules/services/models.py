import uuid

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.shared.database.connection import Base
from src.shared.database.mixins import SoftDeleteMixin, TimestampMixin


class ServiceCategory(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "service_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(80), nullable=False, unique=True, index=True)


class Service(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "services"
    __table_args__ = (
        CheckConstraint("duration_minutes > 0", name="ck_service_duration_positive"),
        CheckConstraint("price >= 0", name="ck_service_price_non_negative"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("service_categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    name = Column(String(120), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
