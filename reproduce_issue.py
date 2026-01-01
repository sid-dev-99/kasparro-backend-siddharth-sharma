import sys
import os
sys.path.append(os.getcwd())
from app.ingestion import transformer
from app.schemas.schemas import CryptoAssetCreate

def test_reproduction_duplicates():
    # Simulate data from different sources for the same asset (Bitcoin)
    
    # CoinPaprika data
    paprika_data = [{
        "id": "btc-bitcoin",
        "name": "Bitcoin",
        "symbol": "BTC",
        "quotes": {"USD": {"price": 50000, "market_cap": 1000000}}
    }]
    
    # CoinGecko data
    gecko_data = [{
        "id": "bitcoin",
        "name": "Bitcoin",
        "symbol": "btc",
        "current_price": 50100,
        "market_cap": 1000100
    }]
    
    # CSV data
    csv_data = [{
        "symbol": "BTC",
        "name": "Bitcoin",
        "price_usd": 50200,
        "market_cap": 1000200
    }]
    
    # Transform
    unified_paprika = transformer.transform_coinpaprika_data(paprika_data)
    unified_gecko = transformer.transform_coingecko_data(gecko_data)
    unified_csv = transformer.transform_csv_data(csv_data)
    
    # Combine (new logic)
    all_unified = transformer.unify_assets(unified_paprika, unified_gecko, unified_csv)
    
    print(f"Total records: {len(all_unified)}")
    for asset in all_unified:
        print(f"ID: {asset.id}, Symbol: {asset.symbol}, Source: {asset.source}")

    # Check for duplicates based on symbol
    symbols = [asset.symbol.upper() for asset in all_unified]
    if symbols.count("BTC") > 1:
        print("FAIL: Duplicate assets found for symbol BTC")
    else:
        print("SUCCESS: No duplicates found")

if __name__ == "__main__":
    test_reproduction_duplicates()
