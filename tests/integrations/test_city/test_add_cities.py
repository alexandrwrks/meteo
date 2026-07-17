import pytest


@pytest.mark.asyncio
async def test_add_cities(client):
    response = await client.post(
        "/auth/register",
        params={
            "username": "citytest2",
        }
    )

    access_token = response.json()["access_token"]

    response = await client.post(
        "/meteo/city",
        params={
            "latitude": 56.50049,
            "longitude": 84.98216,
            "city_name": "Tomsk"
        },
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200

    response = await client.get(
        "/meteo/cities",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Tomsk"

