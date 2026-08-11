from collections.abc import AsyncGenerator
# pyrefly: ignore [missing-import]
from fastapi import Request
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession
# pyrefly: ignore [missing-import]
import redis.asyncio as redis

async def get_redis_session(request: Request) -> redis.Redis:

    # Retrieving the Redis connection pool from app state
    return request.app.state.redis

async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession,None]:

    # Creating a new database session
    
    session_factory = request.app.state.db_session_factory

    # Generate a new session from the session factory.
    async with session_factory() as session:
        yield session
