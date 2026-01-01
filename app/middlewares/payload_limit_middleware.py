from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse
from fastapi import status

class PayloadLimitMiddleware:
    def __init__(self, app: ASGIApp, max_content_size: int = 10 * 1024 * 1024):
        self.app = app
        self.max_content_size = max_content_size

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # only check HTTP requests
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers") or [])
        content_length = None
        if b"content-length" in headers:
            try:
                content_length = int(headers[b"content-length"].decode())
            except ValueError:
                response = JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"error": True, "data": {"message": "Invalid Content-Length header."}},
                )
                await response(scope, receive, send)
                return

        if content_length and content_length > self.max_content_size:
            response = JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={
                    "error": True,
                    "data": {
                        "message": f"Payload too large. "
                                   f"Max allowed size is {self.max_content_size / (1024 * 1024):.2f} MB."
                    },
                },
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)

