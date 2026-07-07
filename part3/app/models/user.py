#!/usr/bin/python3
"""User model module."""

import re
from sqlalchemy.orm import validates
from app import db, bcrypt
from app.models.base_model import BaseModel


class User(BaseModel):
    """User class for the HBnB application."""

    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        """Initialize a User instance."""
        self.places = []
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password:
            self.hash_password(password)

    @validates("first_name")
    def validate_first_name(self, key, value):
        """Validate first name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("first_name is required")
        if len(value) > 50:
            raise ValueError("first_name must be 50 characters or less")
        return value

    @validates("last_name")
    def validate_last_name(self, key, value):
        """Validate last name."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("last_name is required")
        if len(value) > 50:
            raise ValueError("last_name must be 50 characters or less")
        return value

    @validates("email")
    def validate_email(self, key, value):
        """Validate email."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("email is required")

        email = value.strip().lower()
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(pattern, email):
            raise ValueError("email must be valid")

        return email

    @validates("is_admin")
    def validate_is_admin(self, key, value):
        """Validate admin status."""
        if not isinstance(value, bool):
            raise TypeError("is_admin must be a boolean")
        return value

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify if the provided password matches the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def add_place(self, place):
        """Add a place owned by this user."""
        if place not in self.places:
            self.places.append(place)
            self.save()
