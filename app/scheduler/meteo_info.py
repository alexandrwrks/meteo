from app.api.api import meteo_api_client
from app.db.config import new_session
from app.repo.meteo_repo import MeteoRepo


async def update_all_forecasts():
    async with new_session() as session:
        meteo_repo = MeteoRepo(session)

        cities = await meteo_repo.get_cities()

        async with session.begin():
            for city in cities:
                forecast = await meteo_api_client.get_meteo_forecast(
                    latitude=city.latitude,
                    longitude=city.longitude,
                )

                await meteo_repo.remove_forecast(
                    forecast=forecast,
                    city_id=city.id,
                )