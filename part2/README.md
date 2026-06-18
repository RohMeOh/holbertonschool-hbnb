# HBnB - Part 2

This project implements the initial structure and core business logic for the HBnB application.

HBnB is organized using a modular architecture with clear separation between the Presentation, Business Logic, Service, and Persistence layers.

## Project Structure

```text
part2/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── config.py
├── requirements.txt
├── run.py
├── test_models.py
└── README.md
:wq
:q!
