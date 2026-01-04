from fastapi import APIRouter
from app.api.controllers.auth_controller import register, get_user
from app.helpers.schema_validations.auth_schema import authRegisterUsersResponse, authGetUsersResponse

auth_router = APIRouter()

auth_router.post("/registerUsers", response_model=authRegisterUsersResponse, include_in_schema=True)(register)
auth_router.get("/getUsers", response_model=authGetUsersResponse)(get_user)
