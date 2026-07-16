import pytest


@pytest.mark.asyncio
async def test_city(client):
    response = await client.get("/meteo/cities")

    assert response.status_code == 401