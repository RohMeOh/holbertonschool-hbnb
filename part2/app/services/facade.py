#!/usr/bin/python3
"""Facade layer for the HBnB application."""

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
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

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity by ID."""
        amenity = self.get_amenity(amenity_id)

        if not amenity:
            return None

        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    def create_place(self, place_data):
        """Create a new place."""
        owner_id = place_data.get("owner_id")
        owner = self.get_user(owner_id)

        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get("amenities", [])
        amenities = []

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            amenities.append(amenity)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            price=place_data.get("price"),
            latitude=place_data.get("latitude"),
            longitude=place_data.get("longitude"),
            owner=owner
        )

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place by ID."""
        place = self.get_place(place_id)

        if not place:
            return None

        if "owner_id" in place_data:
            owner = self.get_user(place_data["owner_id"])
            if not owner:
                raise ValueError("Owner not found")
            place_data["owner"] = owner
            del place_data["owner_id"]

        if "amenities" in place_data:
            amenities = []

            for amenity_id in place_data["amenities"]:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError("Amenity not found")
                amenities.append(amenity)

            place.amenities = amenities
            del place_data["amenities"]

        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)
