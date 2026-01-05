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

class authGetUsersDataModel(BaseModel):
    users: list
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

class authLoginErrorDataModel(BaseModel):
    message: str

class authLoginResponse(BaseModel):
    error: bool
    data: Union[authLoginDataModel, authLoginErrorDataModel]
    
class authLoginRequest(BaseModel):
    username: str
    email: str
    password: str
