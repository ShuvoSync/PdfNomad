import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase, AsyncAttrs

class Base(DeclarativeBase, AsyncAttrs):
    pass

class BaseModel(Base):
    """
    Abstract base model for all PDF Nomad models.
    Provides UUIDs, timestamps, and soft-delete capabilities.
    """
    __abstract__ = True

    # Using String(36) to ensure seamless compatibility between SQLite and PostgreSQL later
    id = Column(
        String(36), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()), 
        index=True
    )
    
    created_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    updated_at = Column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False
    )

    def soft_delete(self):
        """Deactivates the record without removing it from the database."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def restore(self):
        """Restores a soft-deleted record."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    @property
    def is_deleted(self) -> bool:
        """Returns True if the record has been soft-deleted."""
        return not self.is_active

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"