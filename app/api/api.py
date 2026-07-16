import httpx

from app.utils.schemas.request import CityParams, GeoParams


url = "https://api.open-meteo.com/v1/forecast"
field = ["temperature_2m", "wind_speed_10m", "precipitation", "relative_humidity_2m"]

class MeteoAPIClient:


	def __init__(self):
		self.base_url = url
		self.fields = field

	async def get_meteo_by_coordinates(self, parameters: GeoParams, client: httpx.AsyncClient):
		response = await client.get(
			self.base_url,
			params={
				"latitude": parameters.latitude,
				"longitude": parameters.longitude,
				"current": ["surface_pressure", "temperature_2m", "wind_speed_10m"],
				"timezone": "auto"
			}
		)

		return response.json()

	async def get_meteo_by_coordinates_with_city_name(self, latitude: float, longitude: float, client: httpx.AsyncClient):
		response = await client.get(
			self.base_url,
			params={
				"latitude": latitude,
				"longitude": longitude,
				"hourly": self.fields,
				"timezone": "auto"
			}
		)

		return response.json()

	async def get_meteo_forecast(
			self,
			latitude: float,
			longitude: float,
			client: httpx.AsyncClient,
	):
		response = await client.get(
			self.base_url,
			params={
				"latitude": latitude,
				"longitude": longitude,
				"hourly": self.fields,
				"forecast_days": 1,
				"timezone": "auto"
			}
		)

		return response.json()


meteo_api_client = MeteoAPIClient()
