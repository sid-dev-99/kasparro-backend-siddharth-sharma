from fastapi.testclient import TestClient
from app.main import app
from app.models import CryptoAsset

client = TestClient(app)

def test_health_check(db_session):
    response = client.get("/health", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert "database" in data
    assert "etl" in data

def test_get_data_empty(db_session):
    db_session.query(CryptoAsset).delete()
    db_session.commit()
    
    response = client.get("/data", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["data"] == []
    assert data["pagination"]["total"] == 0

def test_get_data_pagination(db_session):
    db_session.query(CryptoAsset).delete()
    db_session.commit()

    # Seed data
    asset1 = CryptoAsset(id="btc", symbol="BTC", name="Bitcoin", price_usd=50000, market_cap=1000000, source="test")
    asset2 = CryptoAsset(id="eth", symbol="ETH", name="Ethereum", price_usd=3000, market_cap=500000, source="test")
    db_session.add(asset1)
    db_session.add(asset2)
    db_session.commit()

    response = client.get("/data?page=1&limit=1", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["pagination"]["total"] == 2
    assert data["pagination"]["page"] == 1

def test_get_data_filter(db_session):
    db_session.query(CryptoAsset).delete()
    db_session.commit()

    # Seed data
    asset1 = CryptoAsset(id="btc", symbol="BTC", name="Bitcoin", price_usd=50000, market_cap=1000000, source="test")
    db_session.add(asset1)
    db_session.commit()

    response = client.get("/data?symbol=BTC", headers={"X-API-Key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]) == 1
    assert data["data"][0]["symbol"] == "BTC"
