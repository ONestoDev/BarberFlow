import uuid

from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID

from src.shared.database.connection import Base
from src.shared.database.mixins import SoftDeleteMixin, TimestampMixin


class Customer(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
        index=True,
    )
    name = Column(String(120), nullable=False, index=True)
    phone = Column(String(15), nullable=False, unique=True, index=True)
    email = Column(String(160), nullable=True, index=True)
    notes = Column(Text, nullable=True)
