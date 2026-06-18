#!/usr/bin/python3
"""Base model module for common attributes and methods."""

import uuid
from datetime import datetime


class BaseModel:
    """Base class for all HBnB business logic models."""

    def __init__(self):
        """Initialize common attributes."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update object attributes from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        protected_attrs = {"id", "created_at", "updated_at"}

        for key, value in data.items():
            if key not in protected_attrs and hasattr(self, key):
                setattr(self, key, value)

        self.save()
