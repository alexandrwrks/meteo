import jwt
from fastapi import HTTPException

from jwt import PyJWTError, DecodeError
from datetime import datetime, timedelta, timezone

from starlette import status

from app.utils.settings import settings


class JWTService:
    def __init__(self):
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.SECRET_KEY = settings.SECRET_KEY

    def create_token(self, user_id: int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": user_id,
            "exp":  now + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": now,
        }

        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def verify_token(self, credentials: str) -> dict:
        try:
            return jwt.decode(
                credentials,
                self.SECRET_KEY,
                algorithms=[self.ALGORITHM]
            )
        except (PyJWTError, DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

jwt_service = JWTService()