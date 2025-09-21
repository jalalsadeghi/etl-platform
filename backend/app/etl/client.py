import asyncio
from typing import Any, Dict, List, Optional

import httpx
from app.core.settings import settings

RETRIES = 3
BACKOFF = 0.5  # seconds


async def fetch_rows(url: str | None = None) -> list[dict]:
    url = url or settings.ETL_SOURCE_URL
    # simple retry loop
    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(url)
                r.raise_for_status()
                data = r.json()
                # normalize to list[dict]
                if isinstance(data, list):
                    return data
                if isinstance(data, dict):
                    # handle APIs like reqres.in -> {"data":[...]}
                    return data.get("results") or data.get("data") or []
                return []
        except httpx.HTTPError:
            if attempt == 2:
                raise
            await asyncio.sleep(1.5 * (attempt + 1))


async def get_json(url: str, headers: Optional[Dict[str, str]] = None) -> Any:
    for attempt in range(1, RETRIES + 1):
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(url, headers=headers)
                resp.raise_for_status()
                return resp.json()
        except Exception:
            if attempt == RETRIES:
                raise
            await asyncio.sleep(BACKOFF * attempt)


async def fetch_paginated(
    base_url: str, headers: Optional[Dict[str, str]] = None
) -> List[Dict]:
    """
    Generic paginator. For the demo API (jsonplaceholder) there is no pagination,
    so this returns a single page. Keep this in place for real APIs later.
    """
    data = await get_json(base_url, headers=headers)
    if isinstance(data, list):
        return data
    return data.get("results", [])
