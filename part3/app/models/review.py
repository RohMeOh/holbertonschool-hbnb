#!/usr/bin/python3
"""Review model module."""

from sqlalchemy.orm import validates
from app import db
from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    """Review class for the HBnB application."""

    __tablename__ = "reviews"

    text = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

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

    @property
    def place(self):
        """Get the reviewed place."""
        return self._place

    @place.setter
    def place(self, value):
        """Set and validate the reviewed place."""
        if not isinstance(value, Place):
            raise TypeError("place must be a Place instance")
        self._place = value

    @property
    def user(self):
        """Get the review author."""
        return self._user

    @user.setter
    def user(self, value):
        """Set and validate the review author."""
        if not isinstance(value, User):
            raise TypeError("user must be a User instance")
        self._user = value
