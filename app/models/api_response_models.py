from typing import List

from pydantic import BaseModel, ConfigDict


class SimpleWeatherCondition(BaseModel):
    main: str
    description: str


SimpleWeatherCondition.__config__ = ConfigDict(arbitrary_types_allowed=True)


class SimpleForecast(BaseModel):
    date: str
    temperature: float
    feels_like: float
    conditions: List[SimpleWeatherCondition]


SimpleForecast.__config__ = ConfigDict(arbitrary_types_allowed=True)


class WeatherForecastResponse(BaseModel):
    city_name: str
    forecasts: List[SimpleForecast]


WeatherForecastResponse.__config__ = ConfigDict(arbitrary_types_allowed=True)
