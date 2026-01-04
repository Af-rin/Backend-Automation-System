from fastapi import status, Depends
from fastapi.responses import JSONResponse
from app.api.services.auth_service import register_user, get_users_list
from app.helpers.schema_validations.auth_schema import authRegisterUsersRequest
from sqlalchemy.orm import Session
from app.connections.db_connector import get_db

async def register(payload: authRegisterUsersRequest, db: Session = Depends(get_db)):
    try:
        data = payload.dict()
        response_data = await register_user(data=data, db=db)
        return JSONResponse(
            status_code= response_data.get("status_code", 500),
            content=response_data.get("content", {
                    "error": True,
                    "data": {"message": "Internal server error while registering."},
                }),
            )
    except Exception as e:
        print(f"Error while registering :: {str(e)}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "data": {"message": "Internal server error while registering."},
                },
            )

async def get_user(db: Session = Depends(get_db)):
    try:
        response_data = await get_users_list(db=db)
        return JSONResponse(
                status_code=response_data.get("status_code", 500),
                content=response_data.get("content", {
                    "error": True,
                    "data": {"message": "Internal server error while getting users."},
                }),
            )
    except Exception as e:
        print(f"Error while  trying to getting users :: {str(e)}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "data": {"message": "Internal server error while getting users."},
                },
            )