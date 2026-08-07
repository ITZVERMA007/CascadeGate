# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
from httpx import AsyncClient, ASGITransport
from app.main import app

# Tells pytest to run async test
@pytest.fixtures(scope="session")
def anyio_backend():
    return "asyncio"

# Creates an async HTTP client to test the endpoints
@pytest.fixtures(scope="session")
async def async_client():

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url="http://test") as client:
        yield client