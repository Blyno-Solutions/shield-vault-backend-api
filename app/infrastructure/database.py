from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.core.config import settings

if "sqlite" in settings.DATABASE_URL:
    DATABASE_URL = settings.DATABASE_URL
else:
    DATABASE_URL = settings.DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://"
    )

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(  # type: ignore
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
