import pytest
import httpx
from datetime import datetime
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock, patch
from api.main import app

# 1. Mock pour WeatherResponse (Météo actuelle)
MOCK_WEATHER_RESPONSE = {
    "city": "Paris",
    "country": "FR",
    "timestamp": datetime.now().isoformat(),
    "weather": {
        "temperature": 20.5,
        "feels_like": 19.8,
        "humidity": 45.0,
        "pressure": 1013.0,
        "wind_speed": 5.2,
        "description": "Ciel dégagé",
        "icon": "01d"
    }
}

# 2. Mock pour ForecastResponse (Prévisions)
MOCK_FORECAST_RESPONSE = {
    "city": "Lyon",
    "country": "FR",
    "forecast": [
        {
            "date": "2024-03-21",
            "temp_min": 10.0,
            "temp_max": 22.0,
            "temp_day": 21.0,
            "temp_night": 12.0,
            "humidity": 50.0,
            "wind_speed": 3.5,
            "description": "Partiellement nuageux",
            "icon": "02d",
            "precipitation_probability": 10.0
        }
    ]
}

TARGET_PATH = "src.resources.weather_resource.weather_service"


@pytest.mark.asyncio
async def test_get_current_weather_success():
    with patch(f"{TARGET_PATH}.get_current_weather", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_WEATHER_RESPONSE

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/weather/current?city=Paris&country_code=FR")

        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Paris"
        assert data["weather"]["temperature"] == 20.5


@pytest.mark.asyncio
async def test_get_current_weather_not_found():
    with patch(f"{TARGET_PATH}.get_current_weather", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = httpx.HTTPStatusError(
            "Not Found",
            request=None,
            response=httpx.Response(404)
        )

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/weather/current?city=Inconnue")

        assert response.status_code == 404
        assert "non trouvée" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_forecast_success():
    with patch(f"{TARGET_PATH}.get_forecast", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_FORECAST_RESPONSE

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/weather/forecast?city=Lyon")

        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "Lyon"
        assert len(data["forecast"]) > 0
        assert data["forecast"][0]["temp_max"] == 22.0