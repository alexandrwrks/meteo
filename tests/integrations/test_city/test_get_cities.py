import pytest


@pytest.mark.asyncio
async def test_get_cities(client):
    response = await client.post(
        "/auth/register",
        params={
            "username": "citytest1",
        }
    )

    access_token = response.json()["access_token"]

    response = await client.get(
        "/meteo/cities",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json() == []