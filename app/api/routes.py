from fastapi import APIRouter, Depends, Query, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import time
import uuid

from app.core.database import get_db
from app.models import CryptoAsset, ETLStatus
from app.core.database import get_db
from app.models import CryptoAsset, ETLStatus
from app.schemas.schemas import CryptoAssetResponse, ETLStatusResponse, PaginatedResponse, ETLStatsResponse
from app.services import stats_service
from app.ingestion import runner
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/data", response_model=PaginatedResponse)
def get_data(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    symbol: Optional[str] = None,
    db: Session = Depends(get_db)
):
    start_time = time.time()
    request_id = str(uuid.uuid4())

    query = db.query(CryptoAsset)
    
    if symbol:
        query = query.filter(CryptoAsset.symbol == symbol)
    
    total = query.count()
    offset = (page - 1) * limit
    data = query.offset(offset).limit(limit).all()
    
    latency_ms = (time.time() - start_time) * 1000

    return {
        "data": data,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total
        },
        "metadata": {
            "request_id": request_id,
            "api_latency_ms": latency_ms
        }
    }

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Check DB connectivity
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {e}"

    # Check ETL status
    etl_status_record = db.query(ETLStatus).order_by(ETLStatus.last_run.desc()).first()
    
    etl_info = {
        "status": "unknown",
        "last_run": None,
        "error": None
    }
    
    if etl_status_record:
        etl_info["status"] = etl_status_record.status
        etl_info["last_run"] = etl_status_record.last_run
        etl_info["error"] = etl_status_record.error_message

    return {
        "database": db_status,
        "etl": etl_info
    }

@router.get("/stats", response_model=ETLStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    return stats_service.get_etl_stats(db)

@router.get("/metrics", response_class=PlainTextResponse)
def get_metrics(db: Session = Depends(get_db)):
    """Exposes Prometheus-style metrics."""
    return stats_service.generate_prometheus_metrics(db)

@router.get("/runs")
def get_runs(limit: int = 10, db: Session = Depends(get_db)):
    """Lists past ETL runs."""
    return stats_service.get_past_runs(db, limit)

@router.get("/compare-runs")
def compare_runs(run_id_1: int, run_id_2: int, db: Session = Depends(get_db)):
    """Compares two ETL runs."""
    return stats_service.compare_runs(db, run_id_1, run_id_2)

@router.post("/etl/run")
def trigger_etl(background_tasks: BackgroundTasks):
    """Triggers the ETL process in the background."""
    background_tasks.add_task(runner.run_etl)
    return {"message": "ETL process triggered in background"}
