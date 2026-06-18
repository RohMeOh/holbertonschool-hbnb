#!/usr/bin/python3
"""Amenity model module."""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class for the HBnB application."""

    def __init__(self, name):
        """Initialize an Amenity instance."""
        super().__init__()
        self.name = name

    @property
    def name(self):
        """Get the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set and validate the amenity name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or less")
        self._name = value
