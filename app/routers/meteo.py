from datetime import time
from typing import List

from fastapi import APIRouter, Depends, Query

from app.service.meteo_service import MeteoService
from app.utils.deps import get_meteo_service
from app.utils.schemas.schemas import (
    CityParams,
    GeoParams,
    ResponseCitySchema,
    ResponseCurrentMeteoSchema,
    WeatherField, ResponseWeatherSchema
)

router = APIRouter(
    prefix="/meteo",
    tags=["meteo"],
)


@router.get("/current", response_model=ResponseCurrentMeteoSchema)
async def get_meteo_by_coordinate(
    params: GeoParams = Depends(GeoParams),
    meteo_service: MeteoService = Depends(get_meteo_service),
):
    return await meteo_service.get_current_meteo_by_coordinate(params)


@router.get("/cities")
async def get_cities(meteo_service: MeteoService = Depends(get_meteo_service)):
    return await meteo_service.get_cities()


@router.post("/city", response_model=ResponseCitySchema)
async def add_city(
    params: CityParams = Depends(CityParams),
    meteo_service: MeteoService = Depends(get_meteo_service),
):
    return await meteo_service.add_city_parameters(params)


@router.get("/forecast", response_model=ResponseWeatherSchema)
async def get_forecast(
    city_name: str = Query(min_length=1),
    time: time = Query(...),
    params: List[WeatherField] = Query(...),
    meteo_service: MeteoService = Depends(get_meteo_service),
):
    return await meteo_service.get_forecast(city_name, time, params)
