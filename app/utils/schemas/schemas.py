from datetime import datetime

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


class ResponseCurrentMeteoSchema(BaseModel):
    time: str
    surface_pressure: float
    temperature_2m: float
    wind_speed_10m: float

class CityParams(GeoParams):
    city_name: str

class ResponseCitySchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    message: str = "City added successfully"

class ForecastData(BaseModel):
    forecast_time: datetime
    temperature: float
    wind_speed: float
    precipitation: float
    humidity: float
