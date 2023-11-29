from pydantic import BaseModel
from typing import List, Dict, Union


class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class MainInfo(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class WeatherForecast(BaseModel):
    dt: int  # Timestamp da previsão
    main: MainInfo
    weather: List[WeatherCondition]
    clouds: Dict[str, int]
    wind: Dict[str, float]
    sys: Dict[str, str]
    dt_txt: str


class Wind(BaseModel):
    speed: float
    deg: int


class Clouds(BaseModel):
    all: int


class Sys(BaseModel):
    pod: str


class Coord(BaseModel):
    lat: float
    lon: float


class City(BaseModel):
    id: int
    name: str
    coord: Coord
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
