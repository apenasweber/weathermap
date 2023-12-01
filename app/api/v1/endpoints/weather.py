from fastapi import APIRouter, HTTPException, Depends, Query
from app.api.v1.auth.auth_bearer import JWTBearer
from typing import Optional

from app.services.open_weather_service import OpenWeatherMapsAPI
from app.models.api_response_models import (
    WeatherForecastResponse,
    SimpleForecast,
    SimpleWeatherCondition,
)
from app.db.mongo_client import MongoDB
from bson import ObjectId

router = APIRouter()
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_weather_service() -> OpenWeatherMapsAPI:
    return OpenWeatherMapsAPI()


@router.get(
    "/forecast",
    response_model=WeatherForecastResponse,
    dependencies=[Depends(JWTBearer())],
)
def weather_forecast(
    city: Optional[str] = None,
    lat: Optional[float] = Query(None, description="Latitude"),
    lon: Optional[float] = Query(None, description="Longitude"),
    weather_service: OpenWeatherMapsAPI = Depends(get_weather_service),
):
    # Checa se apenas cidade ou apenas latitude e longitude foram fornecidos
    if city and (lat is not None or lon is not None):
        raise HTTPException(
            status_code=400,
            detail="Provide either city name or both latitude and longitude, but not both.",
        )

    # Se apenas cidade é fornecida
    if city:
        forecast_data = weather_service.get_weather_forecast_by_city(city)

    # Se apenas latitude e longitude são fornecidas
    elif lat is not None and lon is not None:
        forecast_data = weather_service.get_weather_forecast_by_coordinates(lat, lon)

    # Se nenhum dos dois é fornecido
    else:
        raise HTTPException(
            status_code=400,
            detail="Either city name or both latitude and longitude must be provided.",
        )

    if forecast_data is None or "list" not in forecast_data:
        raise HTTPException(
            status_code=500, detail="Error fetching data from OpenWeatherMaps"
        )

    forecasts = []
    for forecast in forecast_data["list"]:
        print(type(forecast))
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

    city_name = forecast_data["city"].name if forecast_data["city"] else "Unknown"
    return WeatherForecastResponse(
        city_name=city_name,
        forecasts=forecasts,
    )


# Função para converter ObjectId para string
def convert_objectid_to_str(data):
    if isinstance(data, list):
        logger.info(f"Convertendo lista: {data}")
        return [convert_objectid_to_str(item) for item in data]
    if isinstance(data, dict):
        converted_dict = {
            k: convert_objectid_to_str(v) if k == "_id" else v for k, v in data.items()
        }
        logger.info(f"Convertendo dicionário: {converted_dict}")
        return converted_dict
    if isinstance(data, ObjectId):
        logger.info(f"Convertendo ObjectId: {str(data)}")
        return str(data)
    return data


@router.get(
    "/all", response_model=WeatherForecastResponse, dependencies=[Depends(JWTBearer())]
)
def get_all_weather_data():
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        # Buscando dados do MongoDB
        weather_data = list(weather_collection.find({}))
        # Convertendo ObjectId para string (se necessário)
        weather_data_converted = convert_objectid_to_str(weather_data)

        # Construindo a resposta
        forecasts = []
        for forecast in weather_data_converted:
            for data in forecast.get("list", []):
                conditions = [
                    SimpleWeatherCondition(
                        main=cond["main"], description=cond["description"]
                    )
                    for cond in data.get("weather", [])
                ]
                simple_forecast = SimpleForecast(
                    date=data.get("dt_txt", "Unknown"),
                    temperature=data["main"].get("temp", 0),
                    feels_like=data["main"].get("feels_like", 0),
                    conditions=conditions,
                )
                forecasts.append(simple_forecast)

        return WeatherForecastResponse(
            city_name=weather_data_converted[0].get("city", {}).get("name", "Unknown")
            if weather_data_converted
            else "Unknown",
            forecasts=forecasts,
        )
    except Exception as e:
        logger.error(f"Error occurred while fetching data from the database: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/by-id/{document_id}",
    response_model=WeatherForecastResponse,
    dependencies=[Depends(JWTBearer())],
)
def get_weather_data_by_id(document_id: str):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        document = weather_collection.find_one({"_id": ObjectId(document_id)})
        if not document:
            raise HTTPException(status_code=404, detail="Documento não encontrado")

        document = convert_objectid_to_str(document)

        forecasts = []
        for data in document["list"]:
            conditions = [
                SimpleWeatherCondition(
                    main=cond["main"], description=cond["description"]
                )
                for cond in data["weather"]
            ]
            forecast = SimpleForecast(
                date=data["dt_txt"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                conditions=conditions,
            )
            forecasts.append(forecast)

        return WeatherForecastResponse(
            city_name=document["city"]["name"], forecasts=forecasts
        )
    except Exception as e:
        logger.error("Error occurred while fetching data from the database", exc_info=e)
        raise HTTPException(
            status_code=500, detail="Erro ao buscar dados do banco de dados"
        )


@router.delete("/delete-all", dependencies=[Depends(JWTBearer())])
def delete_all_weather_data():
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        # Deleta todos os documentos na coleção
        deletion_result = weather_collection.delete_many({})
        return {
            "message": f"Total de documentos deletados: {deletion_result.deleted_count}"
        }
    except Exception as e:
        logger.error("Error occurred while deleting data from the database", exc_info=e)
        raise HTTPException(
            status_code=500, detail="Erro ao deletar dados do banco de dados"
        )


@router.delete("/delete-by-id/{document_id}", dependencies=[Depends(JWTBearer())])
def delete_weather_data_by_id(document_id: str):
    try:
        db = MongoDB.get_database()
        weather_collection = db.weather_data
        # Deleta o documento especificado pelo ID
        deletion_result = weather_collection.delete_one({"_id": ObjectId(document_id)})
        if deletion_result.deleted_count == 0:
            raise HTTPException(
                status_code=404, detail="Documento não encontrado ou já deletado"
            )
        return {"message": "Documento deletado com sucesso"}
    except Exception as e:
        logger.error("Error occurred while deleting data from the database", exc_info=e)
        raise HTTPException(
            status_code=500, detail="Erro ao deletar dados do banco de dados"
        )
