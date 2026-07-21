import uuid

from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.dialects.postgresql import UUID

from src.shared.database.connection import Base
from src.shared.database.enums import UserRole
from src.shared.database.mixins import TimestampMixin, SoftDeleteMixin


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name = Column(String(120), nullable=False)
    email = Column(String(160), nullable=False, unique=True, index=True)
    password_hash = Column(Text, nullable=False)

    role = Column(Enum(UserRole, name="user_role"), nullable=False)
