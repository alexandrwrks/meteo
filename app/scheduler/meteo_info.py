import asyncio

import httpx

from app.api.api import meteo_api_client
from app.db.config import new_session
from app.repo.meteo_repo import MeteoRepo


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
                    for i in range(len(hourly["time"])):
                        time = hourly['time'][i]
                        temperature = hourly["temperature_2m"][i]
                        wind_speed = hourly["wind_speed_10m"][i]
                        precipitation = hourly["precipitation"][i]
                        humidity = hourly["relative_humidity_2m"][i]
                        # print(
                        #     f"Время: {hourly['time'][i]}\n"
                        #     f"Температура: {temperature} °C\n"
                        #     f"Скорость ветра: {wind_speed} km/h\n"
                        #     f"Осадки: {precipitation} mm\n"
                        #     f"Влажность: {humidity} %\n"
                        # )

                        conditions.append([time, temperature, wind_speed, precipitation, humidity])

                    print(len(conditions))
                    print(conditions)

                    # Обновление/добавление данных

if __name__ == '__main__':
    asyncio.run(update_all_forecasts())