from typing import List, Dict, Any
from app.schemas.schemas import CryptoAssetCreate

def transform_coinpaprika_data(raw_data: List[Dict[str, Any]]) -> List[CryptoAssetCreate]:
    """Transforms CoinPaprika data to unified schema."""
    transformed = []
    for item in raw_data:
        try:
            # CoinPaprika returns 'id', 'name', 'symbol', 'quotes' -> 'USD' -> 'price'
            price = item.get("quotes", {}).get("USD", {}).get("price", 0)
            market_cap = item.get("quotes", {}).get("USD", {}).get("market_cap", 0)
            
            asset = CryptoAssetCreate(
                id=item["id"],
                symbol=item["symbol"],
                name=item["name"],
                price_usd=price,
                market_cap=market_cap,
                source="coinpaprika"
            )
            transformed.append(asset)
        except Exception as e:
            # Skip malformed items but log error (print for now)
            print(f"Error transforming CoinPaprika item {item.get('id')}: {e}")
            continue
    return transformed

def transform_coingecko_data(raw_data: List[Dict[str, Any]]) -> List[CryptoAssetCreate]:
    """Transforms CoinGecko data to unified schema."""
    transformed = []
    for item in raw_data:
        try:
            # CoinGecko: id, symbol, name, current_price, market_cap
            asset = CryptoAssetCreate(
                id=item["id"],
                symbol=item["symbol"].upper(),
                name=item["name"],
                price_usd=float(item["current_price"]),
                market_cap=float(item["market_cap"]) if item.get("market_cap") else None,
                source="coingecko"
            )
            transformed.append(asset)
        except Exception as e:
            print(f"Error transforming CoinGecko item {item.get('id')}: {e}")
            continue
    return transformed

def transform_csv_data(raw_data: List[Dict[str, Any]]) -> List[CryptoAssetCreate]:
    """Transforms CSV data to unified schema."""
    transformed = []
    for item in raw_data:
        try:
            # CSV columns: symbol, name, price_usd, market_cap
            # We need to generate an ID, let's use symbol as ID for CSV source or generate one
            symbol = item["symbol"]
            asset_id = f"csv-{symbol.lower()}"
            
            asset = CryptoAssetCreate(
                id=asset_id,
                symbol=symbol,
                name=item["name"],
                price_usd=float(item["price_usd"]),
                market_cap=float(item["market_cap"]) if item.get("market_cap") else None,
                source="csv"
            )
            transformed.append(asset)
        except Exception as e:
            print(f"Error transforming CSV item {item}: {e}")
            continue
    return transformed
