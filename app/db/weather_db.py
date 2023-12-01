from app.db.mongo_client import MongoDB
from app.models.api_response_models import WeatherForecastResponse
import logging

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
        logger.info("Weather data saved successfully")

    except Exception as e:
        logger.error("Error occurred while saving the data to database", exc_info=e)
        raise
