from typing import Tuple
import requests
from django.conf import settings
from rest_framework.exceptions import APIException


def fetch_city_temperature(city: str) -> Tuple[float, int] | None:
    base_url = settings.WEATHER_BASE_URL
    params = {
        "q": city,
        "appid": settings.OPENWEATHERMAP_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise APIException(detail=f"Failed to fetch temperature: {e}", code=500)

    data = response.json()

    try:
        temp = float(data["main"]["temp"])
        timezone_offset = data["timezone"]
        return temp, timezone_offset
    except KeyError as e:
        raise APIException(detail=f"Missing expected key: {e}", code=500)
