from app.services import stats_service
from app.models import ETLStatus, ETLCheckpoint
from datetime import datetime

def test_get_etl_stats(db_session):
    # Clear existing data
    db_session.query(ETLStatus).delete()
    db_session.query(ETLCheckpoint).delete()
    db_session.commit()

    # Setup mock data
    status = ETLStatus(status="success", duration_seconds=10.5, last_run=datetime.now())
    db_session.add(status)
    
    cp1 = ETLCheckpoint(source="coinpaprika", status="success", records_processed=100)
    cp2 = ETLCheckpoint(source="coingecko", status="success", records_processed=50)
    db_session.add(cp1)
    db_session.add(cp2)
    db_session.commit()
    
    stats = stats_service.get_etl_stats(db_session)
    
    assert stats.total_records == 150
    assert stats.last_duration_seconds == 10.5
    assert len(stats.checkpoints) == 2
