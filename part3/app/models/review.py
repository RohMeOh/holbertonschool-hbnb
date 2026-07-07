#!/usr/bin/python3
"""Review model module."""

from sqlalchemy.orm import validates
from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review class for the HBnB application."""

    __tablename__ = "reviews"

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)

    def __init__(self, text, rating, place, user):
        """Initialize a Review instance."""
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    @validates("text")
    def validate_text(self, key, value):
        """Validate the review text."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("text is required")
        return value

    @validates("rating")
    def validate_rating(self, key, value):
        """Validate the review rating."""
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("rating must be an integer")
        if value < 1 or value > 5:
            raise ValueError("rating must be between 1 and 5")
        return value
