# Kasparro Backend Deployment Guide

## Prerequisites
- Python 3.10+
- PostgreSQL
- Docker (optional)

## Setup

1.  **Clone the repository**
    ```bash
    git clone <repo-url>
    cd Kasparro-backend
    ```

2.  **Environment Configuration**
    - Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    - **CRITICAL**: Edit `.env` and set a secure `APP_API_KEY`. The application will not start without it.
    - Configure `DATABASE_URL` for your PostgreSQL instance.

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize Data**
    - The application uses a local CSV as one of its data sources. You must populate it before running the ETL.
    - Run the fetch script to get real data from CoinGecko:
        ```bash
        python3 -m app.scripts.fetch_coingecko_data
        ```

## Running the Application

### Local
```bash
uvicorn app.main:app --reload
```

### Docker
```bash
docker-compose up --build
```

## ETL Pipeline
To trigger the ETL pipeline manually:
```bash
python3 -m app.ingestion.runner
```
