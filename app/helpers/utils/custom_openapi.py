from fastapi.openapi.utils import get_openapi
from app.core.config import Settings

def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Backend Automation System",
        version="1.0.0",
        description="""
            Production-ready FastAPI backend for automation workflows with authentication, PostgreSQL, and AWS deployment.
        """,
        routes=app.routes,
    )
    
    if "components" not in openapi_schema:
            openapi_schema["components"] = {}
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    openapi_schema["info"]["x-logo"] = {
        "url": "/static/afrin-logo.svg",
        "backgroundColor": "#0F172A",
        "altText": "Af-rin Logo"
    }

    PUBLIC_PATHS = {"/health", "/healthz", "/ping"}

    for path, methods in openapi_schema["paths"].items():
        if path in PUBLIC_PATHS:
            continue  # do not apply auth

        for method in methods.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema
