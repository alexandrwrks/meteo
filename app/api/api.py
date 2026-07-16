import httpx
from app.schemas import GeoParams, CityParams

main_url = "https://open-meteo.com"
url = "https://api.open-meteo.com/v1/forecast"


class MeteoAPIClient:
	def __init__(self):
		self.base_url = url

	async def get_meteo_by_coordinates(self, parameters: GeoParams, client: httpx.AsyncClient):
		response = await client.get(
			self.base_url,
			params={
				"latitude": parameters.latitude,
				"longitude": parameters.longitude,
				"current": ["surface_pressure", "temperature_2m", "wind_speed_10m"],
			}
			)

		print(response.json())
		return response.json()

	async def get_meteo_by_coordinates_with_city_name(self, parameters: CityParams, client: httpx.AsyncClient):
		response = await client.get(
			self.base_url,
			params={
				"latitude": parameters.latitude,
				"longitude": parameters.longitude,
				"current": ["surface_pressure", "temperature_2m", "wind_speed_10m"],
			}
		)

		return response.json()

	async def get_meteo_forecast(self, latitude: float, longitude: float):
		...
meteo_api_client = MeteoAPIClient()