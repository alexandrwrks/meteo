from datetime import time
from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from app.service.meteo_service import MeteoService
from app.utils.schemas.request import WeatherField


@pytest.mark.asyncio
async def test_forecast_not_found():
    repo = AsyncMock()

    repo.get_city_by_name.return_value = object()

    repo.get_forecast.return_value = None

    service = MeteoService(AsyncMock())
    service.meteo_repo = repo

    with pytest.raises(HTTPException) as err:
        await service.get_forecast(
            city_name="Almaty",
            forecast=time(15, 30),
            params=[
                WeatherField.temperature,
                WeatherField.humidity
            ],
            user_id=1
        )

    print(err.value)
    assert err.value.status_code == 404
    assert err.value.detail == "Forecast not found"


    repo.get_city_by_name.assert_awaited_once()
    repo.get_forecast.assert_awaited_once()