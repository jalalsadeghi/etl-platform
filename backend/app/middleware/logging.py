import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("etl-api")


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        resp = await call_next(request)
        dur_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            '{"method":"%s","path":"%s","status":%s,"ms":%s}',
            request.method,
            request.url.path,
            resp.status_code,
            dur_ms,
        )
        return resp
