import asyncio
from datetime import datetime

import httpx

from app.api.api import meteo_api_client
from app.db.config import new_session
from app.db.models import WeatherHourlyForecast
from app.repo.meteo_repo import MeteoRepo
from app.utils.logger import logger


async def update_all_forecasts():
    async with new_session() as session:
        meteo_repo = MeteoRepo(session)
        async with httpx.AsyncClient() as client:
            async with session.begin():
                cities = await meteo_repo.get_cities()

                for city in cities:
                    forecast = await meteo_api_client.get_meteo_forecast(
                        latitude=city.latitude,
                        longitude=city.longitude,
                        client=client
                    )

                    hourly = forecast['hourly']
                    conditions = []
                    for forecast_time, temperature, humidity, wind_speed, precipitation in zip(
                            hourly["time"],
                            hourly["temperature_2m"],
                            hourly["relative_humidity_2m"],
                            hourly["wind_speed_10m"],
                            hourly["precipitation"],
                    ):
                        conditions.append(
                            WeatherHourlyForecast(
                                city_id=city.id,
                                forecast_time=datetime.fromisoformat(forecast_time),
                                temperature=temperature,
                                wind_speed=wind_speed,
                                precipitation=precipitation,
                                humidity=humidity,
                            )
                        )

                    await meteo_repo.delete_forecast(city.id)
                    session.add_all(conditions)

                    logger.info("Successfully updated meteo forecast")

if __name__ == '__main__':
    asyncio.run(update_all_forecasts())