from app.db.mongo_client import MongoDB
from app.models.api_response_models import WeatherForecastResponse


def save_weather_data(weather_data: WeatherForecastResponse):
    db = MongoDB.get_database()
    weather_collection = db.weather_data
    weather_data_dict = weather_data.model_dump(by_alias=True, exclude_none=True)
    weather_collection.insert_one(weather_data_dict)
