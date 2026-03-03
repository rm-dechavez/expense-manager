from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import ssl

from src.config import settings
from src.expense.models import Base

# Configure SSL for asyncpg
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = True
ssl_context.verify_mode = ssl.CERT_REQUIRED

# Remove SSL parameters from URL and configure them separately
db_url = settings.DATABASE_URL.replace("?sslmode=require&channel_binding=require", "")

engine = create_async_engine(
    db_url,
    echo=True,
    connect_args={"ssl": ssl_context}
)
SessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
