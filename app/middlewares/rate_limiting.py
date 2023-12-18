from fastapi import FastAPI, Request, Response
from limits import RateLimitItemPerMinute
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, limit_string: str):
        super().__init__(app)
        self.limiter = MovingWindowRateLimiter(MemoryStorage())
        self.limit = RateLimitItemPerMinute(limit_string)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        key = f"ratelimit/{client_ip}"

        if not self.limiter.hit(self.limit, key):
            return JSONResponse(content={"error": "Rate limit exceeded"}, status_code=429)

        response = await call_next(request)
        return response