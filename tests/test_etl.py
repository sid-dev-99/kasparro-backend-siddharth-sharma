from app.ingestion import transformer
from app.schemas.schemas import CryptoAssetCreate

def test_transform_coinpaprika_data():
    raw_data = [
        {
            "id": "btc-bitcoin",
            "name": "Bitcoin",
            "symbol": "BTC",
            "quotes": {
                "USD": {
                    "price": 50000.0,
                    "market_cap": 1000000000.0
                }
            }
        }
    ]
    
    result = transformer.transform_coinpaprika_data(raw_data)
    
    assert len(result) == 1
    assert isinstance(result[0], CryptoAssetCreate)
    assert result[0].symbol == "BTC"
    assert result[0].price_usd == 50000.0
    assert result[0].source == "coinpaprika"

def test_transform_csv_data():
    raw_data = [
        {
            "symbol": "ETH",
            "name": "Ethereum",
            "price_usd": "3000.0",
            "market_cap": "500000000.0"
        }
    ]
    
    result = transformer.transform_csv_data(raw_data)
    
    assert len(result) == 1
    assert result[0].symbol == "ETH"
    assert result[0].price_usd == 3000.0
    assert result[0].source == "csv"
