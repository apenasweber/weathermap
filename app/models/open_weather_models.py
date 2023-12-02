from typing import Dict, List

from pydantic import BaseModel, ConfigDict


class WeatherCondition(BaseModel):
    id: int
    main: str
    description: str
    icon: str


WeatherCondition.__config__ = ConfigDict(arbitrary_types_allowed=True)


class MainInfo(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


MainInfo.__config__ = ConfigDict(arbitrary_types_allowed=True)


class WeatherForecast(BaseModel):
    dt: int  # Timestamp da previsão
    main: MainInfo
    weather: List[WeatherCondition]
    clouds: Dict[str, int]
    wind: Dict[str, float]
    sys: Dict[str, str]
    dt_txt: str


WeatherForecast.__config__ = ConfigDict(arbitrary_types_allowed=True)


class Wind(BaseModel):
    speed: float
    deg: int


Wind.__config__ = ConfigDict(arbitrary_types_allowed=True)


class Clouds(BaseModel):
    all: int


Clouds.__config__ = ConfigDict(arbitrary_types_allowed=True)


class Sys(BaseModel):
    pod: str


Sys.__config__ = ConfigDict(arbitrary_types_allowed=True)


class Coord(BaseModel):
    lat: float
    lon: float


Coord.__config__ = ConfigDict(arbitrary_types_allowed=True)


class City(BaseModel):
    id: int
    name: str
    coord: Coord
    country: str
    population: int
    timezone: int
    sunrise: int
    sunset: int


City.__config__ = ConfigDict(arbitrary_types_allowed=True)


class OpenWeatherResponse(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[WeatherForecast]
    city: City


OpenWeatherResponse.__config__ = ConfigDict(arbitrary_types_allowed=True)
