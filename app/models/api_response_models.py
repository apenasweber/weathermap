from pydantic import BaseModel
from typing import List


class SimpleWeatherCondition(BaseModel):
    main: str
    description: str


class SimpleForecast(BaseModel):
    date: str
    temperature: float
    feels_like: float
    conditions: List[SimpleWeatherCondition]


class WeatherForecastResponse(BaseModel):
    city_name: str
    forecasts: List[SimpleForecast]
