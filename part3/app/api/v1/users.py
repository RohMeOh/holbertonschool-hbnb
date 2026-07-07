#!/usr/bin/python3
"""User API endpoints."""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services import facade

api = Namespace("users", description="User operations")

user_create_model = api.model("UserCreate", {
    "first_name": fields.String(required=True, description="First name"),
    "last_name": fields.String(required=True, description="Last name"),
    "email": fields.String(required=True, description="Email"),
    "password": fields.String(required=True, description="Password"),
    "is_admin": fields.Boolean(description="Admin status")
})

user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(description="First name"),
    "last_name": fields.String(description="Last name"),
    "email": fields.String(description="Email"),
    "password": fields.String(description="Password"),
    "is_admin": fields.Boolean(description="Admin status")
})


def user_to_dict(user):
    """Convert a User object to a dictionary without password."""
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "is_admin": user.is_admin
    }


def is_admin():
    """Return True if current JWT belongs to an admin."""
    return get_jwt().get("is_admin", False)


@api.route("/")
class UserList(Resource):
    """Resource for creating and listing users."""

    @jwt_required()
    @api.expect(user_create_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(403, "Admin privileges required")
    def post(self):
        """Create a new user. Admin only."""
        if not is_admin():
            return {"error": "Admin privileges required"}, 403

        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data["email"])
        if existing_user:
            return {"error": "Email already registered"}, 400

        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return user_to_dict(new_user), 201

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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, "User successfully updated")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    def put(self, user_id):
        """Update user information."""
        current_user = get_jwt_identity()
        user_data = api.payload
        admin = is_admin()

        if not admin and current_user != user_id:
            return {"error": "Unauthorized action"}, 403

        if not admin and ("email" in user_data or "password" in user_data):
            return {"error": "You cannot modify email or password"}, 400

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        if admin and "email" in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                return {"error": "Email already in use"}, 400

        if "password" in user_data:
            user.hash_password(user_data["password"])
            del user_data["password"]

        try:
            updated_user = facade.update_user(user_id, user_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return user_to_dict(updated_user), 200
