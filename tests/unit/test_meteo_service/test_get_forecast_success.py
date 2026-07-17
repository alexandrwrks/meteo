import pytest
from datetime import time


from unittest.mock import AsyncMock

from app.service.meteo_service import MeteoService
from app.utils.schemas.request import WeatherField

@pytest.mark.asyncio
async def test_get_forecast_success():
    repo = AsyncMock()

    city = object()

    repo.get_city_by_name.return_value = city
    repo.get_forecast.return_value = [23.5, 70]

    service = MeteoService(AsyncMock())

    service.meteo_repo = repo

    result = await service.get_forecast(
        city_name="Almaty",
        forecast=time(15, 30),
        params=[
            WeatherField.temperature,
            WeatherField.humidity
        ],
        user_id=1
    )

    assert result.temperature == 23.5
    assert result.humidity == 70

    repo.get_city_by_name.assert_awaited_once()
    city_name, forecast_datetime, params = repo.get_forecast.await_args.args

    print(city_name, forecast_datetime, params)
    assert city_name == "Almaty"
    assert forecast_datetime.hour == 15
    assert forecast_datetime.minute == 0
    assert params == [
        WeatherField.temperature,
        WeatherField.humidity,
    ]




