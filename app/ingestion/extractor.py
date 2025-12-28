import requests
import pandas as pd
import json
import os
from typing import List, Dict, Any
from app.core.resilience import retry_with_backoff

COINPAPRIKA_API_URL = "https://api.coinpaprika.com/v1/tickers"
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false"

@retry_with_backoff(retries=3, backoff_factor=2)
def fetch_coinpaprika_data() -> List[Dict[str, Any]]:
    """Fetches data from CoinPaprika API."""
    try:
        # CoinPaprika Free API doesn't strictly require a key, but if provided we use it.
        # Paid plans use 'Authorization' header.
        headers = {}
        api_key = os.getenv("COINPAPRIKA_API_KEY")
        if api_key:
            headers["Authorization"] = api_key
            
        response = requests.get(COINPAPRIKA_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from CoinPaprika: {e}")
        return []

@retry_with_backoff(retries=3, backoff_factor=2)
def fetch_coingecko_data() -> List[Dict[str, Any]]:
    """Fetches data from CoinGecko API."""
    try:
        # CoinGecko Pro uses 'x-cg-pro-api-key' header or 'x_cg_pro_api_key' param.
        # Demo uses 'x-cg-demo-api-key'. We'll support header injection.
        headers = {}
        api_key = os.getenv("COINGECKO_API_KEY")
        if api_key:
            headers["x-cg-demo-api-key"] = api_key
            
        response = requests.get(COINGECKO_API_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        return []

def fetch_csv_data(file_path: str) -> List[Dict[str, Any]]:
    """Reads data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df.to_dict(orient="records")
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
        return []
