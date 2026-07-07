#!/usr/bin/python3
"""User API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "first_name": fields.String(
        required=True,
        description="First name of the user"
    ),
    "last_name": fields.String(
        required=True,
        description="Last name of the user"
    ),
    "email": fields.String(
        required=True,
        description="Email of the user"
    ),
    "password": fields.String(
        required=True,
        description="Password of the user"
    )
})


def user_to_dict(user):
    """Convert a User object to a dictionary."""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }


@api.route("/")
class UserList(Resource):
    """Resource for creating and listing users."""

    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user."""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return {
            "id": new_user.id,
            "message": "User successfully created"
        }, 201

    @api.response(200, "List of users retrieved successfully")
    def get(self):
        """Get all users."""
        users = facade.get_all_users()
        return [user_to_dict(user) for user in users], 200


@api.route("/<user_id>")
class UserResource(Resource):
    """Resource for retrieving and updating one user."""

    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID."""
        user = facade.get_user(user_id)

        if not user:
            return {"error": "User not found"}, 404

        return user_to_dict(user), 200

    @api.expect(user_model, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update user information."""
        user_data = api.payload

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return user_to_dict(updated_user), 200
