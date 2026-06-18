cat > part2/README.md << 'EOF'
# HBnB - Part 2

This project sets up the initial structure for the HBnB application.

## Project Structure

```text
app/
├── api/
│   └── v1/
├── models/
├── services/
└── persistence/
```

## Directories

- `app/`: Contains the core application code.
- `app/api/`: Contains the API layer.
- `app/api/v1/`: Contains version 1 of the API endpoints.
- `app/models/`: Contains the business logic models.
- `app/services/`: Contains the Facade layer.
- `app/persistence/`: Contains the in-memory repository.
- `run.py`: Entry point for running the Flask application.
- `config.py`: Contains configuration classes.
- `requirements.txt`: Contains project dependencies.

## Layers

The project is organized into three main layers:

1. Presentation Layer: API endpoints.
2. Business Logic Layer: Models and application rules.
3. Persistence Layer: Data storage.

The Facade pattern is used in the service layer to simplify communication between these layers.

## Installation

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Application

Run the Flask application with:

```bash
python3 run.py
```

The API documentation will be available at:

```text
/api/v1/
```
EOF
