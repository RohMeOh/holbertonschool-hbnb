#!/usr/bin/python3
"""Unit tests for HBnB API endpoints."""

import unittest
import uuid
from app import create_app


class TestAPIEndpoints(unittest.TestCase):
    """Test user, amenity, place, and review endpoints."""

    def setUp(self):
        """Set up Flask test client."""
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def unique_email(self):
        """Return a unique test email."""
        return f"user-{uuid.uuid4()}@example.com"

    def create_user(self):
        """Create and return a test user."""
        response = self.client.post("/api/v1/users/", json={
            "first_name": "John",
            "last_name": "Doe",
            "email": self.unique_email()
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_amenity(self):
        """Create and return a test amenity."""
        response = self.client.post("/api/v1/amenities/", json={
            "name": f"Wi-Fi-{uuid.uuid4()}"
        })
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def create_place(self):
        """Create and return a test place."""
        user = self.create_user()
        amenity = self.create_amenity()

        response = self.client.post("/api/v1/places/", json={
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user["id"],
            "amenities": [amenity["id"]]
        })

        self.assertEqual(response.status_code, 201)
        return response.get_json(), user, amenity

    def create_review(self):
        """Create and return a test review."""
        place, user, _ = self.create_place()

        response = self.client.post("/api/v1/reviews/", json={
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })

        self.assertEqual(response.status_code, 201)
        return response.get_json(), place, user

    def test_create_user_success(self):
        """Test successful user creation."""
        user = self.create_user()

        self.assertIn("id", user)
        self.assertEqual(user["first_name"], "John")
        self.assertEqual(user["last_name"], "Doe")

    def test_create_user_invalid_data(self):
        """Test user creation with invalid data."""
        response = self.client.post("/api/v1/users/", json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })

        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test duplicate email validation."""
        email = self.unique_email()

        first_response = self.client.post("/api/v1/users/", json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": email
        })

        second_response = self.client.post("/api/v1/users/", json={
            "first_name": "Other",
            "last_name": "User",
            "email": email
        })

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user."""
        response = self.client.get("/api/v1/users/not-found")

        self.assertEqual(response.status_code, 404)

    def test_create_amenity_success(self):
        """Test successful amenity creation."""
        amenity = self.create_amenity()

        self.assertIn("id", amenity)
        self.assertIn("name", amenity)

    def test_create_amenity_invalid_data(self):
        """Test amenity creation with invalid data."""
        response = self.client.post("/api/v1/amenities/", json={
            "name": ""
        })

        self.assertEqual(response.status_code, 400)

    def test_create_place_success(self):
        """Test successful place creation."""
        place, user, amenity = self.create_place()

        self.assertIn("id", place)
        self.assertEqual(place["owner_id"], user["id"])
        self.assertEqual(place["amenities"], [amenity["id"]])

    def test_create_place_invalid_price(self):
        """Test place creation with invalid price."""
        user = self.create_user()

        response = self.client.post("/api/v1/places/", json={
            "title": "Bad Place",
            "description": "Invalid price",
            "price": 0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": user["id"],
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test place creation with invalid latitude."""
        user = self.create_user()

        response = self.client.post("/api/v1/places/", json={
            "title": "Bad Place",
            "description": "Invalid latitude",
            "price": 100.0,
            "latitude": 100.0,
            "longitude": -122.4194,
            "owner_id": user["id"],
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Test place creation with non-existent owner."""
        response = self.client.post("/api/v1/places/", json={
            "title": "Bad Place",
            "description": "Invalid owner",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": "not-found",
            "amenities": []
        })

        self.assertEqual(response.status_code, 400)

    def test_create_review_success(self):
        """Test successful review creation."""
        review, place, user = self.create_review()

        self.assertIn("id", review)
        self.assertEqual(review["place_id"], place["id"])
        self.assertEqual(review["user_id"], user["id"])
        self.assertEqual(review["rating"], 5)

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating."""
        place, user, _ = self.create_place()

        response = self.client.post("/api/v1/reviews/", json={
            "text": "Bad rating",
            "rating": 6,
            "user_id": user["id"],
            "place_id": place["id"]
        })

        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        """Test review creation with empty text."""
        place, user, _ = self.create_place()

        response = self.client.post("/api/v1/reviews/", json={
            "text": "",
            "rating": 5,
            "user_id": user["id"],
            "place_id": place["id"]
        })

        self.assertEqual(response.status_code, 400)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place."""
        review, place, _ = self.create_review()

        response = self.client.get(
            f"/api/v1/places/{place['id']}/reviews"
        )

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], review["id"])

    def test_update_review_success(self):
        """Test successful review update."""
        review, _, _ = self.create_review()

        response = self.client.put(
            f"/api/v1/reviews/{review['id']}",
            json={
                "text": "Amazing stay!",
                "rating": 4
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_review_success(self):
        """Test successful review deletion."""
        review, _, _ = self.create_review()

        delete_response = self.client.delete(
            f"/api/v1/reviews/{review['id']}"
        )
        get_response = self.client.get(
            f"/api/v1/reviews/{review['id']}"
        )

        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(get_response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
