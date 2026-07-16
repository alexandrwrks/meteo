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

    logger.info("Successfully updated meteo forecasts")

async def get_weather_hourly_forecast(city_id: int):
    async with new_session() as session:
        meteo_repo = MeteoRepo(session)
        async with httpx.AsyncClient() as client:
            async with session.begin():
                city = await meteo_repo.get_city_by_id(city_id)

                response = await meteo_api_client.get_meteo_by_coordinates_with_city_name(
                    city.latitude, city.longitude, client
                )

                hourly = response['hourly']
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
                            city_id=city_id,
                            forecast_time=datetime.fromisoformat(forecast_time),
                            temperature=temperature,
                            wind_speed=wind_speed,
                            precipitation=precipitation,
                            humidity=humidity,
                        )
                    )

                    await meteo_repo.delete_forecast(city.id)
                    session.add_all(conditions)

    logger.info("Successfully add forecast for new city")

if __name__ == "__main__":
    asyncio.run(update_all_forecasts())
