#!/usr/bin/python3
"""Place model module."""

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.amenity import Amenity


class Place(BaseModel):
    """Place class for the HBnB application."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        """Initialize a Place instance."""
        super().__init__()
        self.reviews = []
        self.amenities = []
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        owner.add_place(self)

    @property
    def title(self):
        """Get the place title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set and validate the place title."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("title is required")
        if len(value) > 100:
            raise ValueError("title must be 100 characters or less")
        self._title = value

    @property
    def description(self):
        """Get the place description."""
        return self._description

    @description.setter
    def description(self, value):
        """Set and validate the place description."""
        if value is None:
            value = ""
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        self._description = value

    @property
    def price(self):
        """Get the place price."""
        return self._price

    @price.setter
    def price(self, value):
        """Set and validate the place price."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("price must be a number")
        if value <= 0:
            raise ValueError("price must be positive")
        self._price = float(value)

    @property
    def latitude(self):
        """Get the place latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set and validate the place latitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("latitude must be a number")
        if value < -90.0 or value > 90.0:
            raise ValueError("latitude must be between -90.0 and 90.0")
        self._latitude = float(value)

    @property
    def longitude(self):
        """Get the place longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set and validate the place longitude."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("longitude must be a number")
        if value < -180.0 or value > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")
        self._longitude = float(value)

    @property
    def owner(self):
        """Get the place owner."""
        return self._owner

    @owner.setter
    def owner(self, value):
        """Set and validate the place owner."""
        if not isinstance(value, User):
            raise TypeError("owner must be a User instance")
        self._owner = value

    def add_review(self, review):
        """Add a review to the place."""
        from app.models.review import Review

        if not isinstance(review, Review):
            raise TypeError("review must be a Review instance")

        if review.place is not self:
            raise ValueError("review must belong to this place")

        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("amenity must be an Amenity instance")

        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()
