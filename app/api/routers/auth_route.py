from fastapi import APIRouter, Depends
from app.api.controllers.auth_controller import (
    register, get_user, login
)
from app.helpers.schema_validations.auth_schema import (
    authRegisterUsersResponse, authGetUsersResponse,
    authLoginResponse
)
from app.middlewares.auth_middleware import get_current_admin

auth_router = APIRouter()

auth_router.post("/registerUsers", response_model=authRegisterUsersResponse, include_in_schema=False)(register)
auth_router.get("/getUsers", response_model=authGetUsersResponse, dependencies=[Depends(get_current_admin)])(get_user)
auth_router.post("/login", response_model=authLoginResponse)(login)
