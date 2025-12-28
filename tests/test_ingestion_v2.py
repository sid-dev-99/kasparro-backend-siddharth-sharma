from app.ingestion import transformer, loader
from app.models import ETLCheckpoint

def test_transform_coingecko_data():
    raw_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 50000.0,
            "market_cap": 1000000000.0
        }
    ]
    result = transformer.transform_coingecko_data(raw_data)
    assert len(result) == 1
    assert result[0].symbol == "BTC" # Should be uppercase
    assert result[0].source == "coingecko"

def test_checkpoint_update(db_session):
    loader.update_checkpoint(db_session, "test_source", "success", 10)
    
    cp = db_session.query(ETLCheckpoint).filter_by(source="test_source").first()
    assert cp is not None
    assert cp.status == "success"
    assert cp.records_processed == 10
    
    # Update
    loader.update_checkpoint(db_session, "test_source", "failed", 0)
    db_session.refresh(cp)
    assert cp.status == "failed"
