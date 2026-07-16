from enum import StrEnum

from pydantic import BaseModel, Field


class WeatherField(StrEnum):
    temperature = "temperature"
    humidity = "humidity"
    wind_speed = "wind_speed"
    precipitation = "precipitation"


class GeoParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class CityParams(GeoParams):
    city_name: str

