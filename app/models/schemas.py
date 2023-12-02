from typing import Dict, List

from pydantic import BaseModel


class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Main(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class Wind(BaseModel):
    speed: float
    deg: int


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    pod: str


class WeatherForecast(BaseModel):
    dt: int
    main: Main
    weather: List[WeatherCondition]
    clouds: Clouds
    wind: Wind
    sys: Sys
    dt_txt: str


class City(BaseModel):
    id: int
    name: str
    coord: Dict[str, float]
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


class OpenWeatherResponse(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[WeatherForecast]
    city: City
