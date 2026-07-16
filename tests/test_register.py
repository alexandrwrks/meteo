import pytest

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/auth/register",
        params={
            "username": "test"
        }
    )

    assert response.status_code == 200

    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_register_duplicate(client):
    url = "/auth/register"
    params = {
        "username": "user_test"
    }

    await client.post(url=url, params=params)

    response = await client.post(url=url, params=params)

    assert response.status_code == 404