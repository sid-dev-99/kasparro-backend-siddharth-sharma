import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to get DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")

# If not set, try to construct from individual PG* variables (common in some envs)
if not DATABASE_URL:
    user = os.getenv("PGUSER")
    password = os.getenv("PGPASSWORD")
    host = os.getenv("PGHOST")
    port = os.getenv("PGPORT", "5432")
    db_name = os.getenv("PGDATABASE")

    if user and host and db_name:
        logger.info("DATABASE_URL not found, constructing from PG* variables.")
        # Handle password being optional or empty
        auth = f"{user}:{password}" if password else user
        DATABASE_URL = f"postgresql://{auth}@{host}:{port}/{db_name}"
    else:
        logger.warning("DATABASE_URL and PG* variables are missing. Using default localhost connection.")
        DATABASE_URL = "postgresql://user:password@db:5432/crypto_db"

# Log the connection URL (masking password)
if "@" in DATABASE_URL:
    # simple mask
    masked_url = DATABASE_URL.split("@")[1]
    logger.info(f"Connecting to database at: ...@{masked_url}")
else:
    logger.info(f"Connecting to database with URL: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
