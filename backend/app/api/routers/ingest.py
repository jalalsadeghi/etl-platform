from app.core.settings import settings
from app.db.session import SessionLocal
from app.etl.client import fetch_paginated, fetch_rows
from app.etl.load import load_users, upsert_external_users
from app.etl.transform import clean_rows, to_users_df
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ingest", tags=["ingest"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/demo")
async def ingest_demo(db: Session = Depends(get_db)):
    try:
        rows = await fetch_rows()  # uses settings.ETL_SOURCE_URL
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Source fetch failed: {e}")
    df = clean_rows(rows)
    n = load_users(df, db)
    return {"ingested": int(n)}


@router.post("/users-demo")
async def ingest_users_demo(db: Session = Depends(get_db)):
    headers = {}
    if settings.ETL_API_KEY:
        headers["Authorization"] = f"Bearer {settings.ETL_API_KEY}"
    rows = await fetch_paginated(settings.ETL_SOURCE_URL, headers=headers)
    df = to_users_df(rows)
    affected = upsert_external_users(df, db)
    return {"source": settings.ETL_SOURCE_URL, "rows": len(df), "upserted": affected}
