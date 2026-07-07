# HBnB Database Entity-Relationship Diagram

## ER Diagram

```mermaid
erDiagram
    USERS {
        CHAR(36) id PK
        VARCHAR(255) first_name
        VARCHAR(255) last_name
        VARCHAR(255) email UK
        VARCHAR(255) password
        BOOLEAN is_admin
    }

    PLACES {
        CHAR(36) id PK
        VARCHAR(255) title
        TEXT description
        DECIMAL(10,2) price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id FK
    }

    REVIEWS {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
    }

    AMENITIES {
        CHAR(36) id PK
        VARCHAR(255) name UK
    }

    PLACE_AMENITY {
        CHAR(36) place_id PK FK
        CHAR(36) amenity_id PK FK
    }

    USERS ||--o{ PLACES : owns
    USERS ||--o{ REVIEWS : writes
    PLACES ||--o{ REVIEWS : receives
    PLACES ||--o{ PLACE_AMENITY : has
    AMENITIES ||--o{ PLACE_AMENITY : included_in
```

## Explanation

This ER diagram represents the HBnB database schema.

- A User can own many Places.
- A User can write many Reviews.
- A Place can receive many Reviews.
- Places and Amenities have a many-to-many relationship through the PLACE_AMENITY table.
- The SQL schema also enforces a unique `(user_id, place_id)` constraint so a user can only review a place once.
