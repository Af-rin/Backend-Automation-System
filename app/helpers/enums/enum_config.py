from enum import Enum
from typing import List
from app.core.config import settings


class userRegisterToken(str, Enum):
    REGISTRATION_TOKEN = settings.REGISTRATION_TOKEN


class userRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    @classmethod
    def supported_user_roles(cls) -> List[str]:
        return [e.value for e in cls]


class jwtAuth(str, Enum):
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    SECRET_KEY = settings.JWT_SECRET_KEY
    ALGORITHM = settings.JWT_ALGORITHM
