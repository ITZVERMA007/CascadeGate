# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
import pytest_asyncio
# pyrefly: ignore [missing-import]
import respx
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
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


# Db test
@pytest_asyncio.fixture
async def db_session() -> AsyncSession:

    # Creating in-memory db which disappears as soon as the test finishes
    engine = create_async_engine("sqlite+aiosqlite:///:memory",echo=False)

    testing_session_factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with testing_session_factory as session:
        yield session


# Test for groq api
@pytest.fixture
def mock_grop_api():

    with respx.mock(base_url="https://api.groq.com",assert_all_called=False) as respx_mock:
        yield respx_mock