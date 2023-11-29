from typing import Dict, List, Optional
import requests
import logging
from app.core.config import Settings

# Configurando o logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenWeatherMapsAPI:
    def __init__(self) -> None:
        self.open_weather_maps_forecast_url = Settings.OPEN_WEATHER_MAPS_FORECAST_URL
        self.open_weather_maps_api_key: str = Settings.OPEN_WEATHER_API_KEY

    def get_weather_forecast_by_city(self, city: str) -> Optional[List[Dict]]:
        try:
            params: Dict = {
                "q": city,
                "appid": self.open_weather_maps_api_key,
                "units": "metric",
            }
            return self.request_open_weather_api(params)
        except Exception as e:
            logger.error(f"Erro ao obter previsão do tempo por cidade: {e}")
            return None

    def get_weather_forecast_by_coordinates(
        self, lat: float, lon: float
    ) -> Optional[List[Dict]]:
        try:
            params: Dict = {
                "lat": lat,
                "lon": lon,
                "appid": self.open_weather_maps_api_key,
                "units": "metric",
            }
            return self.request_open_weather_api(params)
        except Exception as e:
            logger.error(f"Erro ao obter previsão do tempo por coordenadas: {e}")
            return None

    def request_open_weather_api(self, params: Dict) -> Optional[List[Dict]]:
        try:
            response = requests.get(self.open_weather_maps_forecast_url, params=params)
            response.raise_for_status()  # Levanta uma exceção para respostas de erro HTTP
            data = response.json()
            return data.get("list", [])
        except requests.RequestException as e:
            logger.error(f"Erro na solicitação da API OpenWeather: {e}")
            return None
