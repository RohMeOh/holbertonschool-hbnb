#!/usr/bin/python3
"""Amenity API endpoints."""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(
        required=True,
        description="Name of the amenity"
    )
})


def amenity_to_dict(amenity):
    """Convert an Amenity object to a dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name
    }


@api.route("/")
class AmenityList(Resource):
    """Resource for creating and listing amenities."""

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new amenity."""
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return amenity_to_dict(new_amenity), 201

    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities."""
        amenities = facade.get_all_amenities()
        return [amenity_to_dict(amenity) for amenity in amenities], 200


@api.route("/<amenity_id>")
class AmenityResource(Resource):
    """Resource for retrieving and updating one amenity."""

    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID."""
        amenity = facade.get_amenity(amenity_id)

        if not amenity:
            return {"error": "Amenity not found"}, 404

        return amenity_to_dict(amenity), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity's information."""
        amenity_data = api.payload

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        try:
            facade.update_amenity(amenity_id, amenity_data)
        except (TypeError, ValueError) as error:
            return {"error": str(error)}, 400

        return {"message": "Amenity updated successfully"}, 200
