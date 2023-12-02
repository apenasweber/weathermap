import logging

from app.db.mongo_client import MongoDB
from app.models.api_response_models import WeatherForecastResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_weather_data(weather_data: WeatherForecastResponse):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        # Convertendo o objeto Pydantic para dicionário
        weather_data_dict = weather_data.model_dump(by_alias=True, exclude_none=True)
        # Inserindo os dados no MongoDB
        weather_collection.insert_one(weather_data_dict)
        logger.info("Dados salvos com sucesso!")

    except Exception as e:
        logger.error("Ocorreu um erro ao salvar no banco de dados", exc_info=e)
        raise
