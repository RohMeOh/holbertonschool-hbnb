#!/usr/bin/python3
"""Repository interface and in-memory repository implementation."""

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract repository interface."""

    @abstractmethod
    def add(self, obj):
        """Add an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Get an object by its ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Get all objects from the repository."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update an object by its ID."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete an object by its ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by one of its attributes."""
        pass


class InMemoryRepository(Repository):
    """In-memory repository for storing objects temporarily."""

    def __init__(self):
        """Initialize the storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """Add an object to storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Return an object by ID, or None if not found."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Return all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Update an object using the provided dictionary."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Delete an object from storage."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Return the first object matching an attribute value."""
        return next(
            (
                obj for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None
        )


class SQLAlchemyRepository(Repository):
    """SQLAlchemy repository for database persistence."""

    def __init__(self, model):
        """Initialize repository with a model class."""
        self.model = model

    def add(self, obj):
        """Add an object to the database."""
        from app import db

        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Return an object by ID, or None if not found."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Return all objects from the database."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object using the provided dictionary."""
        from app import db

        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Delete an object from the database."""
        from app import db

        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Return the first object matching an attribute value."""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
