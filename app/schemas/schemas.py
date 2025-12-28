from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class CryptoAssetBase(BaseModel):
    symbol: str
    name: str
    price_usd: float = Field(..., gt=0)
    market_cap: Optional[float] = None

class CryptoAssetCreate(CryptoAssetBase):
    id: str
    source: str

class CryptoAssetResponse(CryptoAssetBase):
    id: str
    source: str
    last_updated: datetime

    class Config:
        from_attributes = True

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class Metadata(BaseModel):
    request_id: str
    api_latency_ms: float

class PaginatedResponse(BaseModel):
    data: List[CryptoAssetResponse]
    pagination: Pagination
    metadata: Metadata

class ETLStatusResponse(BaseModel):
    status: str
    last_run: datetime
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class CheckpointStats(BaseModel):
    source: str
    status: str
    records_processed: int
    last_run: datetime

class ETLStatsResponse(BaseModel):
    total_records: int
    last_duration_seconds: Optional[float]
    last_success: Optional[datetime]
    last_failure: Optional[datetime]
    checkpoints: List[CheckpointStats]
