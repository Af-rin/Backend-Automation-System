from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple, Dict, Any
from jose import jwt, JWTError, ExpiredSignatureError
import logging
from app.helpers.enums.enum_config import jwtAuth

logger = logging.getLogger(__name__)


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> Tuple[str, str]:
    """
    Create a signed JWT access token.

    Returns:
        (token, expiration_time_iso)
    """
    try:
        if "sub" not in data:
            raise ValueError("JWT payload must include 'sub' claim")

        to_encode = data.copy()

        now = datetime.now(timezone.utc)
        expire = (
            now + expires_delta
            if expires_delta
            else now + timedelta(minutes=int(jwtAuth.ACCESS_TOKEN_EXPIRE_MINUTES.value))
        )

        to_encode.update({
            "iat": now,
            "exp": expire,
        })

        encoded_jwt = jwt.encode(
            to_encode,
            jwtAuth.SECRET_KEY.value,
            algorithm=jwtAuth.ALGORITHM.value,
        )

        return encoded_jwt, expire.isoformat()

    except JWTError as exc:
        logger.exception("JWT creation failed")
        raise RuntimeError("Failed to create access token") from exc

    except Exception as exc:
        logger.exception("Unexpected error while creating JWT")
        raise RuntimeError("Internal token generation error") from exc

def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and return payload.

    Raises:
        ValueError: if token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            jwtAuth.SECRET_KEY.value,
            algorithms=[jwtAuth.ALGORITHM.value],
        )
        return payload

    except ExpiredSignatureError:
        logger.warning("JWT verification failed: token expired")
        raise ValueError("Token has expired")

    except JWTError:
        logger.warning("JWT verification failed: invalid token")
        raise ValueError("Invalid authentication token")

    except Exception as exc:
        logger.exception("Unexpected error during token verification")
        raise ValueError("Token verification failed") from exc
