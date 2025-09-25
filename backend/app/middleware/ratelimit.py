import os
import time

from fastapi import HTTPException, Request
from redis import asyncio as aioredis  # <- use redis.asyncio
from starlette.middleware.base import BaseHTTPMiddleware

WINDOW = 60
LIMIT = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        if self.redis is None:
            self.redis = aioredis.from_url(
                os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
                decode_responses=True,
            )
        key = request.headers.get("x-api-key", "anon")
        now = int(time.time() // WINDOW)
        bucket = f"rl:{key}:{now}"
        count = await self.redis.incr(bucket)
        if count == 1:
            await self.redis.expire(bucket, WINDOW)
        if count > LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        return await call_next(request)
