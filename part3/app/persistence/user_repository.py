#!/usr/bin/python3
"""User repository module."""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for User-specific database operations."""

    def __init__(self):
        """Initialize the User repository."""
        super().__init__(User)

    def get_user_by_email(self, email):
        """Return a user by email."""
        return self.model.query.filter_by(email=email.lower()).first()
