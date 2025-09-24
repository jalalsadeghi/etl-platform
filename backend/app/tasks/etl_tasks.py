# backend/app/tasks/etl_tasks.py
from app.core.settings import settings
from app.db.session import SessionLocal
from app.etl.client import fetch_paginated
from app.etl.load import upsert_external_users
from app.etl.transform import to_users_df
from app.tasks.broker import broker


@broker.task
async def run_users_ingest(source_url: str | None = None) -> dict:
    """Background ETL: fetch -> transform -> upsert."""
    url = source_url or settings.ETL_SOURCE_URL
    rows = await fetch_paginated(url)
    df = to_users_df(rows)
    with SessionLocal() as db:  # ensure session per task
        affected = upsert_external_users(df, db)
    return {"source": url, "rows": int(len(df)), "upserted": int(affected)}
