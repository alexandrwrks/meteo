from fastapi import HTTPException

from app.repo.auth_repo import AuthRepo
from app.service.jwt_service import jwt_service
from app.utils.schemas.response import ResponseUserSchema


class AuthService:
    def __init__(self, session):
        self.auth_repo = AuthRepo(session)

    async def register(self, username: str) -> ResponseUserSchema:
        user_exists = await self.auth_repo.get_user(username)
        if user_exists is not None:
            raise HTTPException(status_code=404, detail="User already exists")

        user_id = await self.auth_repo.add_user(username)
        token = jwt_service.create_token(user_id)
        return ResponseUserSchema(access_token=token)

    async def login(self, username: str) -> ResponseUserSchema:
        user_exists = await self.auth_repo.get_user(username)
        if user_exists is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        token = jwt_service.create_token(user_exists.id)
        return ResponseUserSchema(access_token=token)

    async def check_user(self, credentials: str):
        payload = jwt_service.verify_token(credentials)
        user_id = int(payload["sub"])

        user_exists = await self.auth_repo.get_user_by_id(user_id)
        if user_exists is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        return user_exists