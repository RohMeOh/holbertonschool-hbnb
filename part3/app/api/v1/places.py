#!/usr/bin/python3
"""Place API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace("places", description="Place operations")

amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name of the amenity")
})

user_model = api.model("PlaceUser", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner")
})

review_model = api.model("PlaceReview", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place from 1 to 5"),
    "user_id": fields.String(description="ID of the user")
})

place_input_model = api.model("PlaceInput", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "amenities": fields.List(
        fields.String,
        required=False,
        description="List of amenity IDs"
    )
})

place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude of the place"),
    "longitude": fields.Float(description="Longitude of the place"),
    "amenities": fields.List(
        fields.String,
        description="List of amenity IDs"
    )
})

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner": fields.Nested(user_model, description="Owner of the place"),
    "amenities": fields.List(
        fields.Nested(amenity_model),
        description="List of amenities"
    ),
    "reviews": fields.List(
        fields.Nested(review_model),
        description="List of reviews"
    )
})


def owner_to_dict(owner):
    """Convert a User object to a dictionary."""
    return {
        "id": owner.id,
        "first_name": owner.first_name,
        "last_name": owner.last_name,
        "email": owner.email
    }


def amenity_to_dict(amenity):
    """Convert an Amenity object to a dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name
    }


def review_to_dict(review):
    """Convert a Review object to a dictionary for place responses."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user.id
    }


def place_to_short_dict(place):
    """Convert a Place object to a short dictionary."""
    return {
        "id": place.id,
        "title": place.title,
        "price": place.price
    }


def place_to_dict(place):
    """Convert a Place object to a detailed dictionary."""
    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner": owner_to_dict(place.owner),
        "amenities": [
            amenity_to_dict(amenity) for amenity in place.amenities
        ],
        "reviews": [
            review_to_dict(review) for review in place.reviews
        ]
    }


def place_to_create_dict(place):
    """Convert a Place object to the creation response format."""
    return {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner.id,
        "amenities": [
            amenity.id for amenity in place.amenities
        ]
    }


@api.route("/")
class PlaceList(Resource):
    """Resource for creating and listing places."""

    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new place for the authenticated user."""
        place_data = api.payload
        current_user = get_jwt_identity()

        place_data["owner_id"] = current_user

        if "amenities" not in place_data:
            place_data["amenities"] = []

        try:
            new_place = facade.create_place(place_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return place_to_create_dict(new_place), 201

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places."""
        places = facade.get_all_places()
        return [place_to_short_dict(place) for place in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    """Resource for retrieving and updating one place."""

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID."""
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404

        return place_to_dict(place), 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place's information."""
        place_data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if place.owner.id != current_user:
            return {"error": "Unauthorized action"}, 403

        place_data.pop("owner_id", None)

        try:
            facade.update_place(place_id, place_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return {"message": "Place updated successfully"}, 200


@api.route("/<place_id>/reviews")
class PlaceReviewList(Resource):
    """Resource for retrieving reviews of a specific place."""

    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place."""
        reviews = facade.get_reviews_by_place(place_id)

        if reviews is None:
            return {"error": "Place not found"}, 404

        return [review_to_dict(review) for review in reviews], 200
