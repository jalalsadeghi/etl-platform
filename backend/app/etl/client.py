import asyncio

import httpx
from app.core.settings import settings


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
