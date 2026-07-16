from typing import List

import httpx

from datetime import time

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api import meteo_api_client
from app.repo.meteo_repo import MeteoRepo
from app.utils.logger import logger
from app.utils.schemas.schemas import GeoParams, ResponseCurrentMeteoSchema, CityParams, ResponseCitySchema, WeatherField


class MeteoService:
    def __init__(self, session: AsyncSession):
        self.meteo_repo = MeteoRepo(session)

    async def get_current_meteo_by_coordinate(self, params: GeoParams) -> ResponseCurrentMeteoSchema:
        async with httpx.AsyncClient() as client:
            json_data = await meteo_api_client.get_meteo_by_coordinates(params, client)
        current_data = json_data.get("current")

        logger.info("Successful retrieving current meteo")
        return ResponseCurrentMeteoSchema(
            time=current_data.get("time"),
            surface_pressure=current_data.get("surface_pressure"),
            temperature_2m=current_data.get("temperature_2m"),
            wind_speed_10m=current_data.get("wind_speed_10m")
        )

    async def get_cities(self):
        cities = await self.meteo_repo.get_cities()
        if not cities:
            return []

        return cities

    async def add_city_parameters(self, params: CityParams):
        exists_city = await self.meteo_repo.get_city_by_coordinate(params)
        if exists_city:
            logger.error(f"City {params.city_name} already exists")
            raise HTTPException(status_code=400, detail="City already exists")

        city_id = await self.meteo_repo.add_city_with_parameters(params)

        logger.info("Successful addition of a city")
        return ResponseCitySchema(
            id=city_id,
            name=params.city_name,
            latitude=params.latitude,
            longitude=params.longitude,
        )

    async def get_forecast(self, city_name: str, forecast: time, params: List[WeatherField]):
        forecast = await self.meteo_repo.get_forecast(city_name, forecast, params)
        if forecast is None:
            logger.error(f"City {city_name} forecast is empty")
            raise HTTPException(status_code=404, detail="City not found")

        logger.info("Successful retrieving forecast")
        return {
            field.value: value
            for field, value in zip(params, forecast)
        }