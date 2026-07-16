import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.db.models import Base
from tests.database import engine, TestingSessionLocal

from app.main import app
from app.utils.deps import get_new_session

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    async with TestingSessionLocal() as session:
        async with session.begin():
            yield session


@pytest_asyncio.fixture
async def client(session):

    async def override_get_session():
        yield session

    app.dependency_overrides[get_new_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    app.dependency_overrides.clear()