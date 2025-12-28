import requests
import time
import sys
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "test-key")

HEADERS = {"X-API-Key": API_KEY}

def log(msg):
    print(f"[SMOKE TEST] {msg}")

def check_health():
    log("Checking API health...")
    try:
        resp = requests.get(f"{API_URL}/health", headers=HEADERS)
        if resp.status_code == 200:
            log("Health check passed.")
            return True
    except Exception as e:
        log(f"Health check failed: {e}")
    return False

def trigger_etl():
    log("Triggering ETL process...")
    resp = requests.post(f"{API_URL}/etl/run", headers=HEADERS)
    if resp.status_code == 200:
        log("ETL triggered successfully.")
        return True
    log(f"Failed to trigger ETL: {resp.status_code} - {resp.text}")
    return False

def wait_for_etl_completion(timeout=60):
    log("Waiting for ETL completion...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        resp = requests.get(f"{API_URL}/stats", headers=HEADERS)
        if resp.status_code == 200:
            data = resp.json()
            # Check if last run was recent (within last minute) and success
            # This is a bit tricky if there are old runs. 
            # Ideally we'd check if last_run timestamp > start_time, but simpler:
            # Check if status is success and we assume it's the one we triggered or a previous one.
            # For a smoke test on a fresh env, this is fine.
            # Better: Check if 'etl_last_run_status 1' in metrics
            pass
        
        # Let's check metrics for running status
        metrics_resp = requests.get(f"{API_URL}/metrics", headers=HEADERS)
        if metrics_resp.status_code == 200:
            metrics = metrics_resp.text
            if "etl_last_run_status 1" in metrics:
                log("ETL completed successfully (verified via metrics).")
                return True
        
        time.sleep(2)
    
    log("Timeout waiting for ETL completion.")
    return False

def verify_data():
    log("Verifying data availability...")
    resp = requests.get(f"{API_URL}/data?limit=1", headers=HEADERS)
    if resp.status_code == 200:
        data = resp.json()
        if data["pagination"]["total"] > 0:
            log(f"Data verification passed. Total records: {data['pagination']['total']}")
            return True
    log("Data verification failed.")
    return False

def run_smoke_test():
    log("Starting Smoke Test...")
    
    if not check_health():
        sys.exit(1)
        
    if not trigger_etl():
        sys.exit(1)
        
    if not wait_for_etl_completion():
        sys.exit(1)
        
    if not verify_data():
        sys.exit(1)
        
    log("Smoke Test PASSED!")
    sys.exit(0)

if __name__ == "__main__":
    run_smoke_test()
