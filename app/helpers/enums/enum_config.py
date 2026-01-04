from enum import Enum
from typing import List
from app.core.config import Settings


class userRegisterToken(str, Enum):
    REGISTRATION_TOKEN = Settings().REGISTRATION_TOKEN


class userRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"

    @classmethod
    def supported_user_roles(cls) -> List[str]:
        return [e.value for e in cls]

