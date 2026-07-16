from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.config import new_session
from app.service.meteo_service import MeteoService


async def get_new_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        async with session.begin():
            yield session


async def get_meteo_service(
    session: AsyncSession = Depends(get_new_session),
):
    return MeteoService(session)
