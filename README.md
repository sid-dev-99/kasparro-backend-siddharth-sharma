# 🚀 crypto-etl-service

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)

**crypto-etl-service Backend** is a robust, production-ready service designed to ingest, normalize, and serve cryptocurrency data. It aggregates data from multiple sources (CoinPaprika, CoinGecko, CSV), unifies it into a canonical schema, and exposes it via a secure, high-performance REST API.

---

## 🌟 Key Features

*   **🔗 Multi-Source Ingestion**: Seamlessly fetches market data from CoinPaprika, CoinGecko, and local CSVs.
*   **🔄 Identity Unification**: Smartly merges data for the same asset (e.g., "BTC") across different sources into a single, authoritative record.
*   **🛡️ Enterprise-Grade Security**: Fully protected API endpoints using API Key authentication (`X-API-Key`).
*   **⚙️ Robust ETL Pipeline**:
    *   **Resilience**: Exponential backoff and retries for network stability.
    *   **Drift Detection**: Alerts on upstream API schema changes.
    *   **Checkpointing**: Resume capability for interrupted jobs.
*   **📊 Observability**: Built-in endpoints for `/stats`, `/metrics` (Prometheus), and execution history.
*   **🐳 Deployment Ready**: Optimized multi-stage Docker build for secure and lightweight production deployment.

---

## 🚀 Live Demo

Explore the API documentation and test endpoints directly via Swagger UI:

👉 **[Live Swagger UI](https://web-production-b1b7f.up.railway.app/docs)**

### How to Access
1.  Click the **Authorize 🔓** button on the top right.
2.  Enter your **API Key** in the value box.
    > *Note: Contact the administrator for an API key.*
3.  Click **Authorize** and then **Close**.
4.  You are now authenticated! Try the `GET /health` endpoint to verify.

---

## 🛠️ Tech Stack

*   **Framework**: FastAPI (High performance, easy to use)
*   **Database**: PostgreSQL (Reliable relational storage)
*   **ORM**: SQLAlchemy (Pythonic database interaction)
*   **Validation**: Pydantic v2 (Data integrity)
*   **Testing**: Pytest (Comprehensive test suite)
*   **Infrastructure**: Docker & Docker Compose

---

## 🏃‍♂️ Local Development

### Prerequisites
*   Docker & Docker Compose
*   Python 3.10+

### Quick Start

1.  **Clone the repository**
    ```bash
    git clone https://github.com/your-username/kasparro-backend.git
    cd kasparro-backend
    ```

2.  **Configure Environment**
    Copy the example configuration and set your API key:
    ```bash
    cp .env.example .env
    # Edit .env and set a secure APP_API_KEY
    ```

3.  **Start Services**
    ```bash
    docker-compose up --build -d
    ```

4.  **Initialize Data**
    Fetch the latest data from CoinGecko to populate the local source:
    ```bash
    docker-compose exec app python -m app.scripts.fetch_coingecko_data
    ```

5.  **Access the API**
    *   Swagger UI: `http://localhost:8000/docs`
    *   Health Check: `http://localhost:8000/health`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/data` | Retrieve paginated crypto assets with filtering. |
| `GET` | `/stats` | Get current ETL statistics. |
| `GET` | `/metrics` | Prometheus metrics for monitoring. |
| `GET` | `/runs` | List history of ETL execution runs. |
| `POST` | `/etl/run` | Manually trigger the ETL pipeline. |
| `GET` | `/health` | Check system health. |

---

## ☁️ Deployment

This project is configured for seamless deployment on platforms like **Railway** and **Render**.

**Critical**: Ensure you set the `APP_API_KEY` environment variable in your deployment settings. The application will not start without it.

For detailed instructions, see [deployment_guide.md](deployment_guide.md).

---

## 📂 Project Structure

```
├── app/
│   ├── api/            # API Routes
│   ├── core/           # Config, Database, Security
│   ├── ingestion/      # ETL Logic (Extractor, Transformer, Loader)
│   ├── scripts/        # Utility Scripts
│   ├── models.py       # SQLAlchemy Models
│   └── main.py         # App Entrypoint
├── tests/              # Pytest Suite
├── Dockerfile          # Multi-stage build definition
├── docker-compose.yml  # Local dev orchestration
└── requirements.txt    # Python dependencies
```
