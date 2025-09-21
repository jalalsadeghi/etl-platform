from app.db.session import SessionLocal
from app.etl.client import fetch_rows
from app.etl.load import load_users
from app.etl.transform import clean_rows
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
