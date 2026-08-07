# pyrefly: ignore [missing-import]
import pytest

@pytest.mark.asyncio
async def test_health_endpoints(async_client):

    response = await async_client.get("/health")
    data = response.json()

    # Database in not available/unreachable
    if response.status_code == 503:
        assert data["status"] in ["degraded","not_healthy"]
        assert data["redis"] == "down" or data["postgres"] == "down"

    # Database is reachable
    elif response.status_code == 200:
        assert data["status"] == "healthy"
        assert data["redis"] == "connected"
        assert data["postgres"] == "connected"
    
    else:
        pytest.fail(f"Unexpected status: {response.status_code}")

    assert "up_time" in data