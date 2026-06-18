#!/usr/bin/python3
"""Facade layer for the HBnB application."""

from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    """Facade class used to connect API, business logic, and persistence."""

    def __init__(self):
        """Initialize repositories for each resource."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        """Create a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email."""
        return self.user_repo.get_by_attribute("email", email.lower())

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user by ID."""
        user = self.get_user(user_id)

        if not user:
            return None

        if "email" in user_data:
            new_email = user_data["email"].lower()
            existing_user = self.get_user_by_email(new_email)

            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")

        self.user_repo.update(user_id, user_data)
        return self.get_user(user_id)

    def get_place(self, place_id):
        """Fetch a place by ID.

        Logic will be implemented in a later task.
        """
        pass
