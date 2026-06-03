# High-Level Package Diagram

## Diagram

```mermaid
classDiagram

class PresentationLayer {
    API
    Services
}

class HBnBFacade {
    Facade
}

class BusinessLogicLayer {
    User
    Place
    Review
    Amenity
}

class PersistenceLayer {
    Repository
    Database
}

PresentationLayer --> HBnBFacade : Requests
HBnBFacade --> BusinessLogicLayer : Business Logic
BusinessLogicLayer --> PersistenceLayer : Data Access
```

## Layer Responsibilities

### Presentation Layer
Handles user interactions through APIs and services.

### Business Logic Layer
Contains the application's core entities:
- User
- Place
- Review
- Amenity

This layer implements the business rules.

### Persistence Layer
Responsible for storing and retrieving data from the database.

## Facade Pattern

The `HBnBFacade` acts as a unified interface between the Presentation Layer and the Business Logic Layer.

Instead of interacting directly with models, the Presentation Layer communicates with the facade, which simplifies the architecture and reduces coupling.
