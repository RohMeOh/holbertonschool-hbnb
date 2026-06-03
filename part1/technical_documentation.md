# HBnB Evolution - Technical Documentation

## Introduction

This document provides the technical design and architecture for the HBnB Evolution application. It serves as a blueprint for the implementation phase by documenting the system architecture, business logic, and interaction flow between components.

The application follows a layered architecture composed of a Presentation Layer, Business Logic Layer, and Persistence Layer. Communication between layers is facilitated through the Facade design pattern.

---

# High-Level Architecture

## Purpose

The high-level package diagram illustrates the overall structure of the HBnB application and the communication between its layers.

### Layers

#### Presentation Layer

Responsible for handling user interactions through APIs and services.

#### Business Logic Layer

Contains the application's core entities and business rules.

#### Persistence Layer

Responsible for storing and retrieving data from the database.

### Facade Pattern

The HBnBFacade acts as a unified interface between the Presentation Layer and the Business Logic Layer. This design reduces coupling and simplifies communication between system components.

Refer to:

* high_level_package_diagram.md

---

# Business Logic Layer

## Purpose

The Business Logic Layer contains the core entities and rules of the application.

### Entities

#### User

Represents registered users of the application.

Attributes:

* first_name
* last_name
* email
* password
* is_admin

#### Place

Represents a property listed by a user.

Attributes:

* title
* description
* price
* latitude
* longitude

#### Review

Represents feedback submitted by users for places.

Attributes:

* rating
* comment

#### Amenity

Represents features associated with places.

Attributes:

* name
* description

### Common Attributes

All entities inherit:

* id
* created_at
* updated_at

### Relationships

* A User can own multiple Places.
* A User can write multiple Reviews.
* A Place can receive multiple Reviews.
* A Place can have multiple Amenities.
* An Amenity can belong to multiple Places.

Refer to:

* business_logic_class_diagram.md

---

# API Interaction Flow

## User Registration

This sequence diagram illustrates how a new user account is created.

Flow:

1. User submits registration information.
2. API receives the request.
3. Facade validates and processes the request.
4. User entity is created.
5. Data is stored in the database.
6. Success response is returned.

Refer to:

* user_registration_sequence.md

---

## Place Creation

This sequence diagram illustrates the process of creating a new place listing.

Flow:

1. User submits place information.
2. API forwards the request.
3. Facade processes the request.
4. Place entity is created.
5. Data is persisted.
6. Success response is returned.

Refer to:

* place_creation_sequence.md

---

## Review Submission

This sequence diagram illustrates how users submit reviews.

Flow:

1. User submits review information.
2. API receives the request.
3. Business logic validates the review.
4. Review is stored.
5. Success response is returned.

Refer to:

* review_submission_sequence.md

---

## Fetching Places

This sequence diagram illustrates retrieval of places.

Flow:

1. User requests a list of places.
2. API forwards the request.
3. Business logic retrieves matching places.
4. Database returns results.
5. API returns the list to the user.

Refer to:

* fetch_places_sequence.md

---

# Conclusion

This document defines the architecture, business entities, relationships, and interaction flows for the HBnB Evolution application. It serves as the foundation for future implementation and development phases.

