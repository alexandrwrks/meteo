from datetime import time
from typing import List

import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api import meteo_api_client
from app.repo.meteo_repo import MeteoRepo
from app.utils.logger import logger
from app.utils.schemas.request import CityParams, GeoParams, WeatherField

from app.utils.schemas.response import (
    ResponseCitySchema,
    ResponseCurrentMeteoSchema,
    ResponseWeatherSchema
)
from app.utils.upgrade_time import round_to_hour, floor_to_hour


class MeteoService:
    def __init__(self, session: AsyncSession):
        self.meteo_repo = MeteoRepo(session)
        self.session = session

    async def get_current_meteo_by_coordinate(self, params: GeoParams) -> ResponseCurrentMeteoSchema:
        async with httpx.AsyncClient() as client:
            json_data = await meteo_api_client.get_meteo_by_coordinates(params, client)
        current_data = json_data.get("current")

        logger.info("Successful retrieving current meteo")
        return ResponseCurrentMeteoSchema(
            time=current_data.get("time"),
            surface_pressure=current_data.get("surface_pressure"),
            temperature_2m=current_data.get("temperature_2m"),
            wind_speed_10m=current_data.get("wind_speed_10m"),
        )

    async def get_cities(self, user_id: int):
        cities = await self.meteo_repo.get_user_cities(user_id)
        if not cities:
            return []

        return cities

    async def add_city_parameters(self, params: CityParams, user_id: int) -> ResponseCitySchema:
        exists_city = await self.meteo_repo.get_city_by_coordinate(params, user_id)
        if exists_city:
            logger.error(f"City {params.city_name} already exists")
            raise HTTPException(status_code=404, detail="City already exists")

        city_id = await self.meteo_repo.add_city_with_parameters(params, user_id)

        logger.info("Successful addition of a city")
        await self.session.commit()
        return ResponseCitySchema(
            id=city_id,
            name=params.city_name,
            latitude=params.latitude,
            longitude=params.longitude,
        )

    async def get_forecast(
            self, city_name: str, forecast: time, params: List[WeatherField], user_id: int
    ) -> ResponseWeatherSchema:
        city = await self.meteo_repo.get_city_by_name(city_name, user_id)
        if city is None:
            logger.error(f"City {city_name} forecast is empty")
            raise HTTPException(status_code=404, detail="City not found")

        forecast_datetime = floor_to_hour(forecast)
        forecast = await self.meteo_repo.get_forecast(city_name, forecast_datetime, params)
        if forecast is None:
            logger.error(f"City {city_name} forecast is empty")
            raise HTTPException(status_code=404, detail="Forecast not found")

        logger.info("Successful retrieving forecast")
        return ResponseWeatherSchema(
            **{
                field.value: value
                for field, value in zip(params, forecast)
            }
        )