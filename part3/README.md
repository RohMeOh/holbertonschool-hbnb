# HBnB - Part 3

This project implements the RESTful API, authentication, authorization, SQLAlchemy persistence layer, and database schema for the HBnB application.

The application follows a layered architecture with clear separation between the Presentation, Business Logic, Service, and Persistence layers while using SQLAlchemy as the ORM and JWT for authentication.

## Features

- REST API built with Flask-RESTX
- Password hashing with Flask-Bcrypt
- JWT authentication with Flask-JWT-Extended
- Role-based access control (RBAC)
- SQLAlchemy ORM models
- Repository pattern for data persistence
- SQLite development database
- SQL schema generation and seed data
- Mermaid Entity-Relationship diagram

## Project Structure

```text
part3/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── v1/
│   │       ├── amenities.py
│   │       ├── auth.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── users.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── association_tables.py
│   │   ├── amenity.py
│   │   ├── base_model.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── user.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   └── user_repository.py
│   └── services/
│       ├── __init__.py
│       └── facade.py
├── config.py
├── database_diagram.md
├── requirements.txt
├── run.py
├── schema.sql
└── README.md
```

## Technologies Used

- Python 3
- Flask
- Flask-RESTX
- Flask-Bcrypt
- Flask-JWT-Extended
- SQLAlchemy
- SQLite
- Mermaid.js

## Author

Holberton School – HBnB Project (Part 3)
