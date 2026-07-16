import httpx

from datetime import time

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.api import meteo_api_client
from app.repo.meteo_repo import MeteoRepo
from app.schemas import GeoParams, ResponseCurrentMeteoSchema, CityParams, ResponseCitySchema


class MeteoService:
    def __init__(self, session: AsyncSession):
        self.meteo_repo = MeteoRepo(session)

    async def get_current_meteo_by_coordinate(self, params: GeoParams) -> ResponseCurrentMeteoSchema:
        async with httpx.AsyncClient() as client:
            json_data = await meteo_api_client.get_meteo_by_coordinates(params, client)
        current_data = json_data.get("current")

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
            raise HTTPException(status_code=400, detail="City already exists")

        city_id = await self.meteo_repo.add_city_with_parameters(params)

        return ResponseCitySchema(
            id=city_id,
            name=params.city_name,
            latitude=params.latitude,
            longitude=params.longitude,
        )

    async def get_forecast(self, city_name: str, time: time):
        forecast = await self.meteo_repo.get_forecast(city_name, time)
        if forecast is None:
            raise HTTPException(status_code=404, detail="City not found")

        return forecast