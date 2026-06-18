#!/usr/bin/python3
"""Simple tests for HBnB business logic classes."""

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


def test_user_creation():
    """Test User creation."""
    user = User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com"
    )

    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    assert user.id is not None

    print("User creation test passed!")


def test_place_creation():
    """Test Place creation and owner relationship."""
    owner = User(
        first_name="Alice",
        last_name="Smith",
        email="alice.smith@example.com"
    )

    place = Place(
        title="Cozy Apartment",
        description="A nice place to stay",
        price=100,
        latitude=37.7749,
        longitude=-122.4194,
        owner=owner
    )

    assert place.title == "Cozy Apartment"
    assert place.price == 100.0
    assert place.owner == owner
    assert place in owner.places

    print("Place creation test passed!")


def test_review_relationship():
    """Test Review creation and relationship with Place."""
    owner = User(
        first_name="Maria",
        last_name="Rivera",
        email="maria.rivera@example.com"
    )

    place = Place(
        title="Beach House",
        description="Near the ocean",
        price=150,
        latitude=18.4655,
        longitude=-66.1057,
        owner=owner
    )

    review = Review(
        text="Great stay!",
        rating=5,
        place=place,
        user=owner
    )

    place.add_review(review)

    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    assert review.user == owner
    assert review.place == place

    print("Review relationship test passed!")


def test_amenity_relationship():
    """Test Amenity creation and relationship with Place."""
    owner = User(
        first_name="Carlos",
        last_name="Lopez",
        email="carlos.lopez@example.com"
    )

    place = Place(
        title="City Room",
        description="Small room in the city",
        price=75,
        latitude=18.4241,
        longitude=-66.0618,
        owner=owner
    )

    amenity = Amenity(name="Wi-Fi")
    place.add_amenity(amenity)

    assert amenity.name == "Wi-Fi"
    assert len(place.amenities) == 1
    assert place.amenities[0] == amenity

    print("Amenity relationship test passed!")


if __name__ == "__main__":
    test_user_creation()
    test_place_creation()
    test_review_relationship()
    test_amenity_relationship()
