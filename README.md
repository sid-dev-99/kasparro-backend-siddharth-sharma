# Crypto ETL Backend

This project implements a backend service that ingests crypto data from CoinPaprika API and a CSV source, normalizes it, stores it in Postgres, and exposes it via a REST API.

## Features

- **ETL Pipeline**: Fetches data from API and CSV, normalizes it, and stores it in Postgres.
- **Incremental Ingestion**: Uses Upsert logic to update existing records without duplication.
- **REST API**: Exposes data via `GET /data` with pagination and filtering.
- **Health Check**: `GET /health` reports DB connectivity and ETL status.
- **Dockerized**: Runs entirely via Docker Compose.

## Setup & Running

### Prerequisites
- Docker and Docker Compose
- Make (optional, for convenience)

### Commands

1.  **Start the System**:
    ```bash
    make up
    # OR
    docker-compose up --build -d
    ```
    The API will be available at `http://localhost:8000`.
    The ETL pipeline starts automatically in the background.

2.  **Stop the System**:
    ```bash
    make down
    # OR
    docker-compose down
    ```

3.  **Run Tests**:
    ```bash
    make test
    # OR
    docker-compose run --rm app pytest
    ```

## API Endpoints

-   `GET /data`: Retrieve crypto assets.
    -   Query Params: `page` (default 1), `limit` (default 10), `symbol` (optional).
-   `GET /health`: Check system health.

## Design Decisions

-   **FastAPI**: For high performance and easy API creation.
-   **SQLAlchemy**: ORM for database interactions.
-   **Pydantic**: For data validation and schema definition.
-   **Postgres**: Robust relational database.
-   **ETL Runner**: Runs as a background thread on app startup for simplicity in a single-container setup. In a production environment, this would likely be a separate Celery worker or Airflow DAG.
