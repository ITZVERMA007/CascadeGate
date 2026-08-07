import time
from contextlib import asynccontextmanager
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
import redis.asyncio as redis
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.startup_time = time.time()

    # Redis Connection Pool
    app.state.redis = redis.from_url(
        settings.REDIS_URL,
        encoding='utf-8',
        decode_responses=True
    )

    # Postgres Connection Pool
    engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20 # 20 more connections can be created when high traffic is there(they are temporary connections)
    )

    app.state.db_engine = engine

    app.state.db_session_factory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )
    
    print("All connections opened successfully.")
    try:
        yield
    finally:
        print("Shutting down all connections.")

        await app.state.redis.aclose()
        await app.state.db_engine.dispose()
        print("Successful shutdown")