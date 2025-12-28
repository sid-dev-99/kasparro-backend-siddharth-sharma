from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
from app.core.database import engine, Base
from app.api import routes
from app.ingestion import runner
from app.core.security import get_api_key
from fastapi import Depends
import os

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    if os.getenv("DISABLE_AUTO_ETL") != "true":
        etl_thread = threading.Thread(target=runner.run_etl)
        etl_thread.start()
    yield
    # Shutdown logic

app = FastAPI(title="Crypto ETL Backend", lifespan=lifespan)

# Protect all API routes
app.include_router(routes.router, dependencies=[Depends(get_api_key)])

@app.get("/", dependencies=[Depends(get_api_key)])
def read_root():
    return {"message": "Welcome to Crypto ETL Backend. Go to /docs for API docs."}
