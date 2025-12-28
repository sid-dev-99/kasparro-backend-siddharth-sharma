from app.ingestion import transformer

def test_transform_malformed_data():
    # Data missing 'symbol' which is required
    malformed_data = [
        {
            "id": "btc-bitcoin",
            "name": "Bitcoin",
            # "symbol": "BTC", # Missing
            "quotes": {
                "USD": {
                    "price": 50000.0
                }
            }
        }
    ]
    
    # Should not crash, but return empty list or skip the item
    result = transformer.transform_coinpaprika_data(malformed_data)
    assert len(result) == 0
