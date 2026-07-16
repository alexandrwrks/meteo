from typing import AsyncGenerator

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import new_session
from app.service.auth_service import AuthService
from app.service.meteo_service import MeteoService


async def get_new_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        async with session.begin():
            yield session


async def get_meteo_service(
    session: AsyncSession = Depends(get_new_session),
):
    return MeteoService(session)


async def get_auth_service(
        session: AsyncSession = Depends(get_new_session),
):
    return AuthService(session)

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        auth_service: AuthService = Depends(get_auth_service)
):
    return auth_service.check_user(credentials.credentials)
