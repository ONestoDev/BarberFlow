from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func


class TimestampMixin:
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )


class SoftDeleteMixin:
    active = Column(Boolean, nullable=False, server_default="true")
    deleted_at = Column(DateTime(timezone=True), nullable=True)
