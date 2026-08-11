# pyrefly: ignore [missing-import]
import pytest_asyncio
# pyrefly: ignore [missing-import]
from httpx import AsyncClient, ASGITransport
# pyrefly: ignore [missing-import]
from asgi_lifespan import LifespanManager
from app.main import app


# Creates an async HTTP client to test the endpoints
@pytest_asyncio.fixture(scope="session")
async def async_client():

    # Using this to start the connections for testing as well(without starting the actual server)
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport,base_url="http://test") as client:
            yield client