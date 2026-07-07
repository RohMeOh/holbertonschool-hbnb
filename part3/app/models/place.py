#!/usr/bin/python3
"""Place model module."""

from sqlalchemy.orm import validates
from app import db
from app.models.base_model import BaseModel
from app.models.association_tables import place_amenity


class Place(BaseModel):
    """Place class for the HBnB application."""

    __tablename__ = "places"

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    reviews = db.relationship(
        "Review",
        backref="place",
        lazy=True,
        cascade="all, delete-orphan"
    )

    amenities = db.relationship(
        "Amenity",
        secondary=place_amenity,
        lazy="subquery",
        backref=db.backref("places", lazy=True)
    )

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner
    ):
        """Initialize a Place instance."""
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

    @validates("title")
    def validate_title(self, key, value):
        """Validate the place title."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be 100 characters or less")
        return value

    @validates("description")
    def validate_description(self, key, value):
        """Validate the place description."""
        if value is None:
            return ""
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        return value

    @validates("price")
    def validate_price(self, key, value):
        """Validate the place price."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("price must be a number")
        if value <= 0:
            raise ValueError("price must be positive")
        return float(value)

    @validates("latitude")
    def validate_latitude(self, key, value):
        """Validate the place latitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("latitude must be a number")
        if value < -90.0 or value > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        return float(value)

    @validates("longitude")
    def validate_longitude(self, key, value):
        """Validate the place longitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        return float(value)

    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()
