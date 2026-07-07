#!/usr/bin/python3
"""Base model module for common attributes and methods."""

import uuid
from datetime import datetime
from app import db


class BaseModel(db.Model):
    """Base class for all HBnB business logic models."""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update object attributes from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")

        protected_attrs = {"id", "created_at", "updated_at"}

        for key, value in data.items():
            if key not in protected_attrs and hasattr(self, key):
                setattr(self, key, value)

        self.save()
