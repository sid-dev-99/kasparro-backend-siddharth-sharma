from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class RawCoinPaprika(Base):
    __tablename__ = "raw_coinpaprika"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class RawCoinGecko(Base):
    __tablename__ = "raw_coingecko"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class RawCSV(Base):
    __tablename__ = "raw_csv"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    raw_data = Column(JSON) # Storing the row as JSON for simplicity
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True, index=True) # Symbol or unique ID
    symbol = Column(String, index=True)
    name = Column(String)
    price_usd = Column(Float)
    market_cap = Column(Float, nullable=True)
    source = Column(String) # 'coinpaprika' or 'csv'
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class ETLStatus(Base):
    __tablename__ = "etl_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String) # 'running', 'success', 'failed'
    error_message = Column(String, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    last_run = Column(DateTime(timezone=True), server_default=func.now())

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoints"

    source = Column(String, primary_key=True, index=True) # 'coinpaprika', 'coingecko', 'csv'
    last_run = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String) # 'success', 'failed'
    records_processed = Column(Integer, default=0)
    meta_data = Column(JSON, nullable=True) # Renamed from metadata to avoid conflict with SQLAlchemy

