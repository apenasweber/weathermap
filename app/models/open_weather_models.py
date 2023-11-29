from pydantic import BaseModel
from typing import List, Dict


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
    dt_txt: str  # Data e hora da previsão como string


class OpenWeatherResponse(BaseModel):
    cod: str
    message: int
    cnt: int
    list: List[WeatherForecast]
    city: Dict[str, Union[str, int]]
