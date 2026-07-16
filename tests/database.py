from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker, AsyncSession,
)

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)