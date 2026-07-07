#!/usr/bin/python3
"""Review API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(
        required=True,
        description="Rating of the place from 1 to 5"
    ),
    "place_id": fields.String(required=True, description="ID of the place")
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place from 1 to 5")
})


def review_to_dict(review):
    """Convert a Review object to a detailed dictionary."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "user_id": review.user.id,
        "place_id": review.place.id
    }


def review_to_short_dict(review):
    """Convert a Review object to a short dictionary."""
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating
    }


@api.route("/")
class ReviewList(Resource):
    """Resource for creating and listing reviews."""

    @jwt_required()
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Create a new review by the authenticated user."""
        review_data = api.payload
        current_user = get_jwt_identity()

        place = facade.get_place(review_data.get("place_id"))
        if not place:
            return {"error": "Place not found"}, 400

        if place.owner.id == current_user:
            return {"error": "You cannot review your own place."}, 400

        for review in place.reviews:
            if review.user.id == current_user:
                return {"error": "You have already reviewed this place."}, 400

        review_data["user_id"] = current_user

        try:
            new_review = facade.create_review(review_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return review_to_dict(new_review), 201

    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews."""
        reviews = facade.get_all_reviews()
        return [review_to_short_dict(review) for review in reviews], 200


@api.route("/<review_id>")
class ReviewResource(Resource):
    """Resource for retrieving, updating, and deleting one review."""

    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID."""
        review = facade.get_review(review_id)

        if not review:
            return {"error": "Review not found"}, 404

        return review_to_dict(review), 200

    @jwt_required()
    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        """Update a review's information."""
        review_data = api.payload
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        review_data.pop("user_id", None)
        review_data.pop("place_id", None)

        try:
            facade.update_review(review_id, review_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return {"message": "Review updated successfully"}, 200

    @jwt_required()
    @api.response(200, "Review deleted successfully")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review."""
        current_user = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review_id)

        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
