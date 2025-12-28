import difflib
import logging
from typing import List, Dict, Any, Set

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Expected keys for each source
EXPECTED_KEYS = {
    "coinpaprika": {"id", "name", "symbol", "rank", "circulating_supply", "total_supply", "max_supply", "beta_value", "first_data_at", "last_updated", "quotes"},
    "coingecko": {"id", "symbol", "name", "image", "current_price", "market_cap", "market_cap_rank", "fully_diluted_valuation", "total_volume", "high_24h", "low_24h", "price_change_24h", "price_change_percentage_24h", "market_cap_change_24h", "market_cap_change_percentage_24h", "circulating_supply", "total_supply", "max_supply", "ath", "ath_change_percentage", "ath_date", "atl", "atl_change_percentage", "atl_date", "roi", "last_updated"},
    "csv": {"symbol", "name", "price_usd", "market_cap"}
}

def detect_drift(source: str, data: List[Dict[str, Any]]) -> None:
    """
    Checks for schema drift in the provided data against expected keys.
    Logs warnings if unexpected keys are found or expected keys are missing.
    """
    if not data:
        return

    # Check the first item to infer schema
    sample_item = data[0]
    actual_keys = set(sample_item.keys())
    expected = EXPECTED_KEYS.get(source, set())

    if not expected:
        logger.warning(f"No expected schema defined for source: {source}")
        return

    # Check for missing keys
    missing_keys = expected - actual_keys
    if missing_keys:
        logger.warning(f"[{source}] Schema Drift Detected! Missing keys: {missing_keys}")

    # Check for unexpected keys
    unexpected_keys = actual_keys - expected
    if unexpected_keys:
        logger.warning(f"[{source}] Schema Drift Detected! Unexpected keys: {unexpected_keys}")
        
        # Fuzzy match to see if it's a typo
        for unexpected in unexpected_keys:
            matches = difflib.get_close_matches(unexpected, expected, n=1, cutoff=0.8)
            if matches:
                logger.warning(f"[{source}] Possible typo detected: '{unexpected}' might be '{matches[0]}'")
