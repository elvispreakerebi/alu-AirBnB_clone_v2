"""
This module defines a base class for all hbnb models.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models

Base = declarative_base()

class BaseModel(Base):
    """A base class for all hbnb models."""
    __abstract__ = True  # This makes sure BaseModel is not created as a table
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == "__class__":
                continue  # Skip setting the __class__ attribute
            setattr(self, key, value)

    def save(self):
        """Saves an instance to the current storage."""
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary representation of the instance."""
        return {
            key: value
            for key, value in self.__dict__.items()
            if key != "_sa_instance_state"
        }