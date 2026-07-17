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