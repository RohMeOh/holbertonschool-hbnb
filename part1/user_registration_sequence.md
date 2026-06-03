# User Registration Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant API
    participant HBnBFacade
    participant UserModel
    participant Database

    User->>API: POST /users
    API->>HBnBFacade: register_user(data)
    HBnBFacade->>UserModel: create_user(data)
    UserModel->>Database: save(user)
    Database-->>UserModel: success
    UserModel-->>HBnBFacade: user created
    HBnBFacade-->>API: success response
    API-->>User: 201 Created
```

## Description

This diagram illustrates the process of user registration. The request flows from the API layer through the facade and business logic layer before being stored in the database.
