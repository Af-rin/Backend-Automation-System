import asyncio
from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

class TimeoutMiddleware(BaseHTTPMiddleware):
    # by default 10s timeout
    def __init__(self, app, timeout: int = 10):
        super().__init__(app)
        self.timeout = timeout

    async def dispatch(self, request: Request, call_next):
        try:
            if request.url.path == "/favicon.ico":
                return await call_next(request)
            
            return await asyncio.wait_for(call_next(request), timeout=self.timeout)
        except asyncio.TimeoutError:
            return JSONResponse(
            content={
                "error": True, 
                "data": {
                    "message": "Request timed out after 10 seconds"
                    }
                },
            status_code = status.HTTP_408_REQUEST_TIMEOUT
            )
        
