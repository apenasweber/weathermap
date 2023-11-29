from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.services.open_weather_service import OpenWeatherMapsAPI
from app.models.open_weather_models import OpenWeatherResponse
from app.models.api_response_models import (
    WeatherForecastResponse,
    SimpleForecast,
    SimpleWeatherCondition,
)

router = APIRouter()


def get_weather_service() -> OpenWeatherMapsAPI:
    return OpenWeatherMapsAPI()


@router.get("/forecast", response_model=WeatherForecastResponse)
def weather_forecast(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    weather_service: OpenWeatherMapsAPI = Depends(get_weather_service),
):
    open_weather_data: OpenWeatherResponse = (
        weather_service.get_weather_forecast_by_city(city)
        if city
        else weather_service.get_weather_forecast_by_coordinates(lat, lon)
    )

    if open_weather_data is None or open_weather_data.list is None:
        raise HTTPException(
            status_code=500, detail="Error fetching data from OpenWeatherMaps"
        )
    forecasts = []
    for forecast in open_weather_data.list:
        conditions = [
            SimpleWeatherCondition(main=cond.main, description=cond.description)
            for cond in forecast.weather
        ]
        simple_forecast = SimpleForecast(
            date=forecast.dt_txt,
            temperature=forecast.main.temp,
            feels_like=forecast.main.feels_like,
            conditions=conditions,
        )
        forecasts.append(simple_forecast)

    return WeatherForecastResponse(
        city_name=open_weather_data.city.get("name", "Unknown"),
        forecasts=forecasts,
    )
