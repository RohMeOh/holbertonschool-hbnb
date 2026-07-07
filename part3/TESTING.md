# HBnB Part 2 - Testing and Validation Report

## Objective

This document summarizes the testing and validation performed for the HBnB Part 2 API.

The tested resources are:

- Users
- Amenities
- Places
- Reviews

## Validation Summary

### User

Validation rules:

- `first_name` is required.
- `last_name` is required.
- `email` is required.
- `email` must use a valid format.
- `email` must be unique.

### Amenity

Validation rules:

- `name` is required.
- `name` must be 50 characters or less.

### Place

Validation rules:

- `title` is required.
- `price` must be a positive number.
- `latitude` must be between -90.0 and 90.0.
- `longitude` must be between -180.0 and 180.0.
- `owner_id` must reference an existing user.
- amenities must reference existing amenities.

### Review

Validation rules:

- `text` is required.
- `rating` must be an integer between 1 and 5.
- `user_id` must reference an existing user.
- `place_id` must reference an existing place.

## Swagger Documentation

Swagger documentation can be viewed while the Flask app is running:

```text
http://127.0.0.1:5000/api/v1/
