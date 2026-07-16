from pydantic import BaseModel


class ResponseWeatherSchema(BaseModel):
    temperature: float | None = None
    humidity: float | None = None
    wind_speed: float | None = None
    precipitation: float | None = None


class ResponseCurrentMeteoSchema(BaseModel):
    time: str
    surface_pressure: float
    temperature_2m: float
    wind_speed_10m: float


class ResponseCitySchema(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    message: str = "City added successfully"

class ResponseUserSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"