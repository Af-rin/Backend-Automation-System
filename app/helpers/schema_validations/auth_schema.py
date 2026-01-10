from pydantic import BaseModel
from typing import Union
from app.helpers.enums.enum_config import userRegisterToken, userRoles

class dataModel(BaseModel):
    user_id: int
    message: str

class authRegisterUsersResponse(BaseModel):
    error: bool
    data: dataModel

class authRegisterUsersRequest(BaseModel):
    user_name: str
    email: str
    password: str
    registration_token: userRegisterToken
    role: userRoles

class PaginationModel(BaseModel):
    total_users: int
    page: int
    items_per_page: int

class authGetUsersDataModel(BaseModel):
    users: list
    pagination: PaginationModel
    message: str

class authGetUsersErrorDataModel(BaseModel):
    message: str

class authGetUsersResponse(BaseModel):
    error: bool
    data: Union[authGetUsersDataModel, authGetUsersErrorDataModel]


class authLoginDataModel(BaseModel):
    access_token: str
    token_type: str
    expires_in_utc: str

class ErrorDataModel(BaseModel):
    message: str

class authLoginResponse(BaseModel):
    error: bool
    data: Union[authLoginDataModel, ErrorDataModel]
    
class authLoginRequest(BaseModel):
    username: str
    email: str
    password: str


class UserDataModel(BaseModel):
    _id: str
    username: str
    email: str
    is_active: bool
    lastLogin: str
    createdAt: str

class MeModel(BaseModel):
    user: UserDataModel

class authMeResponse(BaseModel):
    error: bool
    data: Union[MeModel, ErrorDataModel]