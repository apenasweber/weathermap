from typing import Dict, List, Optional
import requests
import logging
from app.db.weather_db import save_weather_data
from app.models.open_weather_models import OpenWeatherResponse
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenWeatherMapsAPI:
    def __init__(self) -> None:
        self.open_weather_maps_forecast_url = settings.OPEN_WEATHER_MAPS_FORECAST_URL
        self.open_weather_maps_api_key: str = settings.OPEN_WEATHER_API_KEY

    def get_weather_forecast_by_city(self, city: str) -> Optional[List[Dict]]:
        try:
            logger.info(f"Iniciando busca de previsão do tempo para a cidade: {city}")
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

    def request_open_weather_api(self, params: Dict) -> Optional[Dict]:
        try:
            response = requests.get(self.open_weather_maps_forecast_url, params=params)
            response.raise_for_status()
            data = response.json()
            weather_data = OpenWeatherResponse(**data)

            logger.info(f"Dados da previsão do tempo processados: {weather_data}")

            # Salva os dados no MongoDB
            logger.info("Preparando para salvar dados de previsão do tempo")
            save_weather_data(weather_data)
            logger.info("Dados de previsão do tempo salvos com sucesso")

            return {"list": weather_data.list, "city": weather_data.city}
        except requests.RequestException as e:
            logger.error(f"Erro na solicitação da API OpenWeather: {e}")
            return None
