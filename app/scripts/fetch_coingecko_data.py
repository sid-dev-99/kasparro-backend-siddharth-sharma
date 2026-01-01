import requests
import csv
import os
import sys

# Mapping of symbols to CoinGecko IDs
SYMBOL_TO_ID = {
    "BTC": "bitcoin",
    "ETH": "ethereum",
    "DOGE": "dogecoin",
    "SOL": "solana"
}

CSV_PATH = os.path.join(os.path.dirname(__file__), "../data/source.csv")

def fetch_data():
    """Fetches current market data from CoinGecko."""
    ids = ",".join(SYMBOL_TO_ID.values())
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ids,
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from CoinGecko: {e}")
        sys.exit(1)

def update_csv(data):
    """Updates the source.csv file with fetched data."""
    # Create a dictionary for quick lookup by ID
    data_map = {item['id']: item for item in data}
    
    rows = []
    for symbol, coin_id in SYMBOL_TO_ID.items():
        if coin_id in data_map:
            item = data_map[coin_id]
            rows.append({
                "symbol": symbol,
                "name": item['name'],
                "price_usd": item['current_price'],
                "market_cap": item['market_cap']
            })
        else:
            print(f"Warning: No data found for {symbol} ({coin_id})")

    if not rows:
        print("No data to write.")
        return

    # Write to CSV
    try:
        with open(CSV_PATH, 'w', newline='') as csvfile:
            fieldnames = ['symbol', 'name', 'price_usd', 'market_cap']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"Successfully updated {CSV_PATH} with {len(rows)} records.")
    except IOError as e:
        print(f"Error writing to CSV: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("Fetching data from CoinGecko...")
    data = fetch_data()
    update_csv(data)
