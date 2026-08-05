import time
from contextlib import asynccontextmanager
# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
import redis.asyncio as redis
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.startup_time = time.time()

    # Redis Connection Pool
    app.state.redis = redis.from_url(
        settings.REDIS_URL,
        encoding='utf-8',
        decode_response=True
    )

    # Postgres Connection Pool
    app.state.db_engine = create_async_engine(
        settings.DATABASE_URL,
        pool_size=10,
        max_overflow=20 # 20 more connections can be created when high traffic is there(they are temporary connections)
    )
    print("All connections opened successfully.")
    yield
    print("Shutting down all connections.")

    await app.state.redis.aclose()
    await app.state.db_engine.dispose()
    print("Successful shutdown")