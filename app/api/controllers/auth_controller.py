from fastapi import Query, status, Depends
from fastapi.responses import JSONResponse
from app.api.services.auth_service import (
    register_user, get_users_list, login_user,
    get_user_profile
)
from app.helpers.schema_validations.auth_schema import (
    authRegisterUsersRequest, authLoginRequest
)
from sqlalchemy.orm import Session
from app.connections.db_connector import get_db
from app.middlewares.auth_middleware import get_current_user
from app.models.user_model import UserModel

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

async def get_user(page: int = Query(1, ge=1), items_per_page: int = Query(20, ge=1, le=100),db: Session = Depends(get_db)):
    try:
        response_data = await get_users_list(db=db, page=page, items_per_page=items_per_page,)
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
    
async def login(payload: authLoginRequest, db: Session = Depends(get_db)):
    try:
        data = payload.dict()
        response_data = await login_user(data=data, db=db)
        return JSONResponse(
                status_code=response_data.get("status_code", 500),
                content=response_data.get("content", {
                    "error": True,
                    "data": {"message": "Internal server error while trying to login."},
                }),
            )
    except Exception as e:
        print(f"Error while  trying to login :: {str(e)}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "data": {"message": "Internal server error while  trying to login."},
                },
            )
    
async def user_profile(current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        response_data = await get_user_profile(data=current_user, db=db)
        return JSONResponse(
                status_code=response_data.get("status_code", 500),
                content=response_data.get("content", {
                    "error": True,
                    "data": {"message": "Internal server error while trying to fetch current user."},
                }),
            )
    except Exception as e:
        print(f"Error while  trying to fetch me :: {str(e)}")
        return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": True,
                    "data": {"message": "Internal server error while trying to fetch me."},
                },
            )