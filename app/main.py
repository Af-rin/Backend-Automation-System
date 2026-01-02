from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings 
import uvicorn
from app.helpers.loggers.logging_config import setup_logging
from app.middlewares.logging_middleware import RotationalLoggerMiddleware
from app.middlewares.timeout_middleware import TimeoutMiddleware
from app.middlewares.payload_limit_middleware import PayloadLimitMiddleware
from app.helpers.utils.custom_openapi import custom_openapi
from app.api.health import router as health_router
from fastapi.staticfiles import StaticFiles
from app.connections.db_connector import init_db, shutdown_db

setup_logging()

# app initialize
app = FastAPI(
    title="Backend Automation System",
    description="Production-ready FastAPI backend for automation workflows with authentication, PostgreSQL, and AWS deployment.",
    version="1.0.0",
)
base_router = Settings().API_PREFIX

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# rotational logger initialize using middleware
app.add_middleware(RotationalLoggerMiddleware)

# Cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], 
    allow_methods = ["GET", "POST"],
    allow_headers = ["*"],
    allow_credentials = True,
)

# timeout middleware initialize with 10s
app.add_middleware(TimeoutMiddleware, timeout=10)

# max payload size limit middleware with 10MB
app.add_middleware(PayloadLimitMiddleware, max_content_size=10 * 1024 * 1024)

# custom swagger / openapi
app.openapi = lambda: custom_openapi(app=app)

@app.on_event("startup")
async def startup_event():
    base_url = Settings().BASE_URL
    print(f"FastAPI application '{app.title}' is now running!")
    print(
        f"Base URL: {base_url}, Swagger Docs: {base_url}/docs, ReDoc Docs: {base_url}/redoc"
    )
    # db initialize
    init_db()

@app.on_event("shutdown")
def shutdown():
    # graceful shutdown
    shutdown_db()

# Health check router
app.include_router(prefix=f"{base_router}", router=health_router)

# Common exception handler
app.exception_handler(Exception)

if __name__ == "__main__":
    port = int(Settings().PORT)
    uvicorn.run("api.main:app", host = "0.0.0.0", port = port, reload=True)


