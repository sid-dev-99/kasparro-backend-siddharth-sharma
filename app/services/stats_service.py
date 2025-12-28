from sqlalchemy.orm import Session
from app.models import ETLStatus, ETLCheckpoint
from app.schemas.schemas import ETLStatsResponse, CheckpointStats

def get_etl_stats(db: Session) -> ETLStatsResponse:
    # Get last run status
    last_run = db.query(ETLStatus).order_by(ETLStatus.last_run.desc()).first()
    
    # Get last success and failure
    last_success = db.query(ETLStatus).filter(ETLStatus.status == "success").order_by(ETLStatus.last_run.desc()).first()
    last_failure = db.query(ETLStatus).filter(ETLStatus.status == "failed").order_by(ETLStatus.last_run.desc()).first()
    
    # Get checkpoints
    checkpoints = db.query(ETLCheckpoint).all()
    
    total_records = sum(cp.records_processed for cp in checkpoints)
    
    checkpoint_stats = [
        CheckpointStats(
            source=cp.source,
            status=cp.status,
            records_processed=cp.records_processed,
            last_run=cp.last_run
        ) for cp in checkpoints
    ]
    
    return ETLStatsResponse(
        total_records=total_records,
        last_duration_seconds=last_run.duration_seconds if last_run else None,
        last_success=last_success.last_run if last_success else None,
        last_failure=last_failure.last_run if last_failure else None,
        checkpoints=checkpoint_stats
    )

def generate_prometheus_metrics(db: Session) -> str:
    """Generates Prometheus metrics text."""
    metrics = []
    
    # ETL Status
    last_run = db.query(ETLStatus).order_by(ETLStatus.last_run.desc()).first()
    status_val = 1 if last_run and last_run.status == "success" else 0
    metrics.append(f'etl_last_run_status {status_val}')
    
    if last_run and last_run.duration_seconds:
        metrics.append(f'etl_last_run_duration_seconds {last_run.duration_seconds}')

    # Checkpoints
    checkpoints = db.query(ETLCheckpoint).all()
    for cp in checkpoints:
        metrics.append(f'etl_records_processed{{source="{cp.source}"}} {cp.records_processed}')
        
    return "\n".join(metrics)

def get_past_runs(db: Session, limit: int):
    """Returns a list of past ETL runs."""
    runs = db.query(ETLStatus).order_by(ETLStatus.last_run.desc()).limit(limit).all()
    return runs

def compare_runs(db: Session, run_id_1: int, run_id_2: int):
    """Compares two runs."""
    run1 = db.query(ETLStatus).filter(ETLStatus.id == run_id_1).first()
    run2 = db.query(ETLStatus).filter(ETLStatus.id == run_id_2).first()
    
    if not run1 or not run2:
        return {"error": "One or both run IDs not found"}
        
    return {
        "run_1": {
            "id": run1.id,
            "status": run1.status,
            "duration": run1.duration_seconds,
            "timestamp": run1.last_run
        },
        "run_2": {
            "id": run2.id,
            "status": run2.status,
            "duration": run2.duration_seconds,
            "timestamp": run2.last_run
        },
        "diff": {
            "duration_diff": (run1.duration_seconds or 0) - (run2.duration_seconds or 0)
        }
    }
