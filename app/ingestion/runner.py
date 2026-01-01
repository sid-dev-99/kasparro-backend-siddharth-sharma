from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.ingestion import extractor, transformer, loader, drift
import os
import time

def run_etl():
    """Runs the full ETL pipeline."""
    db = SessionLocal()
    start_time = time.time()
    try:
        print("Starting ETL pipeline...")
        loader.update_etl_status(db, "running")

        # 1. Extract
        print("Extracting data...")
        api_data = extractor.fetch_coinpaprika_data()
        drift.detect_drift("coinpaprika", api_data)
        
        gecko_data = extractor.fetch_coingecko_data()
        drift.detect_drift("coingecko", gecko_data)
        
        csv_path = os.path.join(os.path.dirname(__file__), "../data/source.csv")
        csv_data = extractor.fetch_csv_data(csv_path)
        drift.detect_drift("csv", csv_data)

        # 2. Load Raw
        print("Loading raw data...")
        if api_data:
            loader.load_raw_coinpaprika(db, api_data)
        if gecko_data:
            loader.load_raw_coingecko(db, gecko_data)
        
        if csv_data:
            loader.load_raw_csv(db, csv_data)

        # Failure Injection (P2.2)
        if os.getenv("INJECT_FAILURE") == "true":
            raise Exception("Simulated ETL Failure (INJECT_FAILURE=true)")

        # 3. Transform
        print("Transforming data...")
        unified_api = transformer.transform_coinpaprika_data(api_data)
        loader.update_checkpoint(db, "coinpaprika", "success", len(unified_api))
        
        unified_gecko = transformer.transform_coingecko_data(gecko_data)
        loader.update_checkpoint(db, "coingecko", "success", len(unified_gecko))
        
        unified_csv = transformer.transform_csv_data(csv_data)
        loader.update_checkpoint(db, "csv", "success", len(unified_csv))
        
        all_unified = transformer.unify_assets(unified_api, unified_gecko, unified_csv)

        # 4. Load Unified
        print(f"Loading {len(all_unified)} unified records...")
        loader.load_unified_data(db, all_unified)

        duration = time.time() - start_time
        loader.update_etl_status(db, "success", duration=duration)
        print(f"ETL pipeline completed successfully in {duration:.2f}s.")

    except Exception as e:
        print(f"ETL pipeline failed: {e}")
        duration = time.time() - start_time
        loader.update_etl_status(db, "failed", str(e), duration=duration)
    finally:
        db.close()

if __name__ == "__main__":
    run_etl()
