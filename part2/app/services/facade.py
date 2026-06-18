#!/usr/bin/python3
"""Facade layer for the HBnB application."""

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
        """Create a user.

        Logic will be implemented in a later task.
        """
        pass

    def get_place(self, place_id):
        """Fetch a place by ID.

        Logic will be implemented in a later task.
        """
        pass
