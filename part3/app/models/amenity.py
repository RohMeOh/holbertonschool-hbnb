#!/usr/bin/python3
"""Amenity model module."""

from sqlalchemy.orm import validates
from app import db
from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity class for the HBnB application."""

    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize an Amenity instance."""
        self.name = name

    @validates("name")
    def validate_name(self, key, value):
        """Validate the amenity name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("name is required")
        if len(value) > 50:
            raise ValueError("name must be 50 characters or less")
        return value
