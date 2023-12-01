import pytest
from unittest.mock import patch, MagicMock
from app.services.open_weather_service import OpenWeatherMapsAPI
import requests
import pytest
from unittest.mock import patch, MagicMock
from app.services.open_weather_service import OpenWeatherMapsAPI
import requests
from app.models.open_weather_models import OpenWeatherResponse
from app.services.open_weather_service import (
    save_weather_data,
)

# Constants for tests
VALID_CITY = "Berlin"
VALID_LAT = 52.5200
VALID_LON = 13.4050
INVALID_CITY = "Atlantis"
INVALID_LAT = -1000.0
INVALID_LON = -1000.0
API_KEY = "test_api_key"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Sample response data
SAMPLE_WEATHER_DATA = {
    "cod": "200",
    "message": 0,
    "cnt": 7,
    "list": [
        {
            "dt": 1618317040,
            "main": {
                "temp": 31.1,
                "feels_like": 36.4,
                "temp_min": 30.0,
                "temp_max": 32.0,
                "pressure": 1012,
                "humidity": 80,
            },
            "weather": [
                {
                    "id": 800,
                    "main": "Clouds",
                    "description": "scattered clouds",
                    "icon": "01d",
                }
            ],
            "clouds": {"all": 10},
            "wind": {"speed": 5.0, "deg": 220},
            "sys": {"pod": "d"},
            "dt_txt": "2023-12-01 21:00:00",
        },
    ],
    "city": {
        "id": 123,
        "name": "Canoas",
        "coord": {"lat": 52.52, "lon": 13.405},
        "country": "DE",
        "population": 1000000,
        "timezone": 3600,
        "sunrise": 1618288262,
        "sunset": 1618334863,
    },
}


@pytest.mark.parametrize(
    "test_id, city, expected_result",
    [
        ("happy_path_valid_city", VALID_CITY, SAMPLE_WEATHER_DATA),
        ("edge_case_empty_city", "", None),
        ("error_case_invalid_city", INVALID_CITY, None),
    ],
)
@pytest.fixture
def open_weather_api():
    api = OpenWeatherMapsAPI()
    api.open_weather_maps_api_key = API_KEY
    api.open_weather_maps_forecast_url = FORECAST_URL
    return api


def test_network_failure(open_weather_api):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError

        result = open_weather_api.get_weather_forecast_by_city(VALID_CITY)
        assert result is None

        result = open_weather_api.get_weather_forecast_by_coordinates(
            VALID_LAT, VALID_LON
        )
        assert result is None


def test_response_validation(open_weather_api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {"invalid": "data"}
        mock_get.return_value = mock_response

        result = open_weather_api.get_weather_forecast_by_city(VALID_CITY)
        assert result is None


def test_process_weather_forecast_by_city(open_weather_api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = SAMPLE_WEATHER_DATA
        mock_get.return_value = mock_response

        with patch("app.services.open_weather_service.save_weather_data") as mock_save:
            result = open_weather_api.get_weather_forecast_by_city(VALID_CITY)
            assert result is not None
            # Acessar a instância de City e em seguida o atributo 'name'
            assert result["city"].name == "Canoas"
            mock_save.assert_called_once()


@pytest.mark.parametrize(
    "test_id, city, expected_result",
    [
        ("happy_path_valid_city", VALID_CITY, SAMPLE_WEATHER_DATA),
        ("edge_case_empty_city", "", None),
        ("error_case_invalid_city", INVALID_CITY, None),
    ],
)
def test_get_weather_forecast_by_city(test_id, city, expected_result, open_weather_api):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        if expected_result:
            mock_response.json.return_value = expected_result
            mock_response.raise_for_status = MagicMock()
        else:
            mock_response.raise_for_status.side_effect = (
                requests.exceptions.RequestException("Error")
            )
        mock_get.return_value = mock_response

        result = open_weather_api.get_weather_forecast_by_city(city)

        if expected_result:
            result_converted = {
                "list": [forecast.model_dump() for forecast in result["list"]],
                "city": result["city"].model_dump(),
            }
            expected_result_converted = {
                "list": expected_result["list"],
                "city": expected_result["city"],
            }
            assert result_converted == expected_result_converted
        else:
            assert result is None


def test_save_weather_data():
    with patch("app.db.mongo_client.MongoDB.get_database") as mock_get_database:
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db.weather_data = mock_collection
        mock_get_database.return_value = mock_db

        weather_data = OpenWeatherResponse(**SAMPLE_WEATHER_DATA)
        save_weather_data(weather_data)

        mock_collection.insert_one.assert_called_once()
