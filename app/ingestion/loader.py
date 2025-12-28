from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func
from app.models import CryptoAsset, RawCoinPaprika, RawCoinGecko, RawCSV, ETLStatus, ETLCheckpoint
from app.schemas.schemas import CryptoAssetCreate
from typing import List
import json

def load_raw_coinpaprika(db: Session, data: List[dict]):
    """Stores raw CoinPaprika data."""
    # For raw data, we might just want to store the whole batch or individual items.
    # Storing individual items for better querying in raw table.
    # To avoid massive bloat, we might clear old raw data or just append. 
    # Requirement: "Store raw data".
    for item in data:
        raw_entry = RawCoinPaprika(data=item)
        db.add(raw_entry)
    db.commit()

def load_raw_coingecko(db: Session, data: List[dict]):
    """Stores raw CoinGecko data."""
    for item in data:
        raw_entry = RawCoinGecko(data=item)
        db.add(raw_entry)
    db.commit()

def load_raw_csv(db: Session, data: List[dict]):
    """Stores raw CSV data."""
    for item in data:
        raw_entry = RawCSV(symbol=item.get("symbol"), raw_data=item)
        db.add(raw_entry)
    db.commit()

def load_unified_data(db: Session, assets: List[CryptoAssetCreate]):
    """Upserts unified data into crypto_assets table."""
    for asset in assets:
        stmt = insert(CryptoAsset).values(
            id=asset.id,
            symbol=asset.symbol,
            name=asset.name,
            price_usd=asset.price_usd,
            market_cap=asset.market_cap,
            source=asset.source
        )
        
        # Postgres UPSERT
        stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_={
                'price_usd': stmt.excluded.price_usd,
                'market_cap': stmt.excluded.market_cap,
                'last_updated': stmt.excluded.last_updated # This will update the timestamp
            }
        )
        db.execute(stmt)
    db.commit()

def update_etl_status(db: Session, status: str, error: str = None, duration: float = None):
    etl_status = ETLStatus(status=status, error_message=error, duration_seconds=duration)
    db.add(etl_status)
    db.commit()

def update_checkpoint(db: Session, source: str, status: str, records: int = 0, meta: dict = None):
    """Updates the checkpoint for a specific source."""
    stmt = insert(ETLCheckpoint).values(
        source=source,
        status=status,
        records_processed=records,
        meta_data=meta,
        last_run=func.now()
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=['source'],
        set_={
            'status': stmt.excluded.status,
            'records_processed': stmt.excluded.records_processed,
            'meta_data': stmt.excluded.meta_data,
            'last_run': stmt.excluded.last_run
        }
    )
    db.execute(stmt)
    db.commit()
