from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import os

# Load database URL from environment variables or config
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/gossip_game")

# Create an async database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency to get async session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session