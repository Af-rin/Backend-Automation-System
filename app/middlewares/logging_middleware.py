import json
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class RotationalLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        # Use the same logger configured in logging_config
        self.logger = logging.getLogger("rotational_logger")

    async def dispatch(self, request, call_next):
        start_time = time.time()

        body_bytes = await request.body()
        try:
            body_text = body_bytes.decode("utf-8")
        except Exception:
            body_text = str(body_bytes)

        # Rebuild receive method so downstream code still sees the body
        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}
        request._receive = receive

        try:
            response = await call_next(request)
        except Exception as e:
            self.logger.exception(f"Unhandled exception at {request.url}: {e}")
            raise

        resp_body = b""
        async for chunk in response.body_iterator:
            resp_body += chunk

        # Rebuild response to pass back to FastAPI
        response = Response(
            content=resp_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

        try:
            resp_text = resp_body.decode("utf-8")
        except Exception:
            resp_text = str(resp_body)

        latency = round(time.time() - start_time, 3)

        log_entry = {
            "method": request.method,
            "url": str(request.url),
            "ip": request.client.host if request.client else None,
            "query_params": dict(request.query_params),
            "request_body": body_text,
            "response_body": resp_text,
            "status_code": response.status_code,
            "latency_seconds": latency,
        }

        self.logger.info(json.dumps(log_entry, ensure_ascii=False))
        return response
