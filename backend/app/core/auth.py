# backend/app/core/auth.py
from app.core.settings import settings
from fastapi import Header, HTTPException


async def api_key_auth(x_api_key: str | None = Header(None)):
    if not settings.API_KEY or x_api_key != settings.API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
