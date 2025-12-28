# Crypto ETL Backend

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)

A robust, production-ready backend service that ingests cryptocurrency data from multiple sources (CoinPaprika, CoinGecko, CSV), normalizes it, and exposes it via a secure REST API.

**Live Demo:** [https://web-production-b1b7f.up.railway.app/docs](https://web-production-b1b7f.up.railway.app/docs)  
**How to use:**
1.  Click the **Authorize** button on the top right.
2.  Enter `test-key` in the value box.
3.  Click **Authorize** and then **Close**.
4.  Now you can try any endpoint (e.g., `GET /health`)!

## 🚀 Features

*   **Multi-Source Ingestion**: Fetches market data from CoinPaprika API, CoinGecko API, and local CSV files.
*   **Robust ETL Pipeline**:
    *   **Resilience**: Implements retries with exponential backoff for API calls.
    *   **Drift Detection**: Automatically detects and logs schema changes in upstream APIs.
    *   **Checkpointing**: Tracks ETL run status to resume or analyze failures.
*   **Secure API**: Protected by API Key authentication (`X-API-Key` header).
*   **Observability**:
    *   `/stats`: Real-time ETL statistics.
    *   `/metrics`: Prometheus-compatible metrics endpoint.
    *   `/runs`: History of past ETL execution runs.
*   **Deployment Ready**: Dockerized and configured for easy deployment on Railway, AWS, or DigitalOcean.

## 🛠️ Tech Stack

*   **Framework**: FastAPI
*   **Database**: PostgreSQL (via SQLAlchemy ORM)
*   **Validation**: Pydantic v2
*   **Testing**: Pytest
*   **Containerization**: Docker & Docker Compose

## 🔑 Authentication

All API endpoints are protected. You must include the `X-API-Key` header in your requests.

```bash
curl -H "X-API-Key: your-secret-key" http://localhost:8000/data
```

*Default key for local development: `test-key`*

## 🏃‍♂️ Local Setup

### Prerequisites
*   Docker & Docker Compose
*   Make (optional)

### Quick Start

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/kasparro-backend.git
    cd kasparro-backend
    ```

2.  **Start with Docker**:
    ```bash
    make up
    # OR
    docker-compose up --build -d
    ```

3.  **Access the API**:
    *   Swagger UI: `http://localhost:8000/docs`
    *   Health Check: `http://localhost:8000/health`

4.  **Run Tests**:
    ```bash
    make test
    ```

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/data` | Retrieve paginated crypto assets with filtering. |
| `GET` | `/stats` | Get current ETL statistics (total records, sources). |
| `GET` | `/metrics` | Prometheus metrics for monitoring. |
| `GET` | `/runs` | List history of ETL execution runs. |
| `GET` | `/compare-runs` | Compare data between two specific ETL runs. |
| `POST` | `/etl/run` | Manually trigger the ETL pipeline (background task). |
| `GET` | `/health` | Check database connectivity and system status. |

## ☁️ Deployment

This project is deployed on **Railway**.

**Base URL:** `https://web-production-b1b7f.up.railway.app`

*   **Web Service**: Handles API requests.
*   **Cron Service**: Runs the ETL pipeline every hour.
*   **PostgreSQL**: Managed database.

For detailed deployment instructions, see [deployment_guide.md](deployment_guide.md).

## 📂 Project Structure

```
├── app/
│   ├── api/            # API Routes
│   ├── core/           # Config, Database, Security
│   ├── ingestion/      # ETL Logic (Extractor, Transformer, Loader)
│   ├── models.py       # SQLAlchemy Models
│   ├── schemas/        # Pydantic Schemas
│   └── main.py         # App Entrypoint
├── tests/              # Pytest Suite
├── data/               # Local data sources (CSV)
├── Dockerfile
├── docker-compose.yml
├── Procfile            # Railway Deployment Config
└── start.sh            # Startup Script
```
