# Detailed Class Diagram for Business Logic Layer

## Diagram

```mermaid
classDiagram

class BaseModel {
    +UUID id
    +datetime created_at
    +datetime updated_at
    +save()
    +update()
}

class User {
    +string first_name
    +string last_name
    +string email
    +string password
    +bool is_admin
    +register()
    +update_profile()
    +delete()
}

class Place {
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +create()
    +update()
    +delete()
    +list()
}

class Review {
    +int rating
    +string comment
    +create()
    +update()
    +delete()
    +list()
}

class Amenity {
    +string name
    +string description
    +create()
    +update()
    +delete()
    +list()
}

User --|> BaseModel
Place --|> BaseModel
Review --|> BaseModel
Amenity --|> BaseModel

User "1" --> "*" Place : owns
User "1" --> "*" Review : writes
Place "1" --> "*" Review : receives
Place "*" --> "*" Amenity : has
```

## Explanatory Notes

### BaseModel
BaseModel contains the common attributes shared by all entities: `id`, `created_at`, and `updated_at`.

### User
The User entity represents a registered user. A user has a first name, last name, email, password, and `is_admin` status.

### Place
The Place entity represents a property listed by a user. It has a title, description, price, latitude, longitude, and an owner.

### Review
The Review entity represents feedback left by a user for a place. It includes a rating and a comment.

### Amenity
The Amenity entity represents features that can be linked to places, such as WiFi, parking, or a pool.

## Relationships

A User can own many Places.

A User can write many Reviews.

A Place can receive many Reviews.

A Place can have many Amenities, and an Amenity can belong to many Places.
