import logging

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routers.ingest import router as ingest_router
from app.db.session import engine

logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","time":"%(asctime)s","logger":"%(name)s","msg":"%(message)s"}',
)
logger = logging.getLogger("etl-api")

app = FastAPI(title="ETL API", version="0.2.0")


@app.get("/health/liveness")
def liveness():
    return {"status": "alive"}


@app.get("/health/readiness")
def readiness():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready", "db": "ok"}
    except Exception as e:
        logger.exception("DB readiness check failed")
        return {"status": "degraded", "db": "error", "detail": str(e)}


app.include_router(ingest_router)
