#!/usr/bin/python3
"""Application factory for the HBnB API."""


def create_app():
    """Create and configure the Flask application."""
    from flask import Flask
    from flask_restx import Api

    app = Flask(__name__)

    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API',
        doc='/api/v1/'
    )

    # Placeholder for API namespaces.
    # Endpoints for users, places, reviews, and amenities will be added later.

    return app
