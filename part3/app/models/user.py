#!/usr/bin/python3
"""User model module."""

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User class for the HBnB application."""

    _used_emails = set()

    def __init__(self, first_name, last_name, email, is_admin=False):
        """Initialize a User instance."""
        super().__init__()
        self.places = []
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Get the user's first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set and validate the user's first name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be 50 characters or less")
        self._first_name = value

    @property
    def last_name(self):
        """Get the user's last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set and validate the user's last name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be 50 characters or less")
        self._last_name = value

    @property
    def email(self):
        """Get the user's email."""
        return self._email

    @email.setter
    def email(self, value):
        """Set and validate the user's email."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("email is required")

        email = value.strip().lower()
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, email):
            raise ValueError("email must be valid")

        current_email = getattr(self, "_email", None)

        if email != current_email and email in User._used_emails:
            raise ValueError("email must be unique")

        if current_email in User._used_emails:
            User._used_emails.remove(current_email)

        User._used_emails.add(email)
        self._email = email

    @property
    def is_admin(self):
        """Get admin status."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Set and validate admin status."""
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        self._is_admin = value

    def add_place(self, place):
        """Add a place owned by this user."""
        if place not in self.places:
            self.places.append(place)
            self.save()
