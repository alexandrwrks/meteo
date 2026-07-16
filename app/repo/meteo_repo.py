from datetime import time
from typing import List

from sqlalchemy import select, and_, insert, Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Cities, WeatherHourlyForecast
from app.schemas import GeoParams, CityParams, WeatherField


class MeteoRepo:
    FIELD_MAPPING = {
        WeatherField.temperature: WeatherHourlyForecast.temperature,
        WeatherField.humidity: WeatherHourlyForecast.humidity,
        WeatherField.wind_speed: WeatherHourlyForecast.wind_speed,
        WeatherField.precipitation: WeatherHourlyForecast.precipitation,
    }

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_meteo_by_coordinate(self, params: GeoParams):
        """Выдаём данные по координатам"""
        result = await self.session.execute(
            select(WeatherHourlyForecast)
            .join(Cities, Cities.id == WeatherHourlyForecast.city_id)
            .where(
                Cities.longitude == params.longitude,
                Cities.latitude == params.latitude,
            )
        )

        return result.scalars().all()

    async def get_city_by_coordinate(self, params: CityParams) -> Cities | None:
        result = await self.session.execute(
            select(Cities)
            .where(
                and_(
                    Cities.name == params.city_name,
                    Cities.latitude == params.latitude,
                    Cities.longitude == params.longitude,
                )
            )
        )

        return result.scalar_one_or_none()

    async def get_cities(self) -> List[Cities]:
        result = await self.session.execute(
            select(Cities)
            .order_by(Cities.id)
        )

        return result.scalars().all()

    async def add_city_with_parameters(self, params: CityParams) -> int:
        result = await self.session.execute(
            insert(Cities)
            .values(
                name=params.city_name,
                latitude=params.latitude,
                longitude=params.longitude,
            )
            .returning(Cities.id)
        )

        return result.scalar_one()

    async def get_forecast(self, city_name: str, forecast: time, params: List[WeatherField]) -> WeatherHourlyForecast | None:
        columns = [self.FIELD_MAPPING[field] for field in params]

        query = (
            select(*columns)
            .join(Cities, Cities.id == WeatherHourlyForecast.city_id)
            .where(
                Cities.name == city_name,
                WeatherHourlyForecast.forecast_time == forecast,
            )
        )

        result = await self.session.execute(query)

        return result.scalar_one_or_none()