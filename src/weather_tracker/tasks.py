import logging

from django.conf import settings

from celery import shared_task

from weather_tracker.services import fetch_city_temperature
from weather_tracker.models import TemperatureRecord


logger = logging.getLogger(__name__)


@shared_task
def fetch_and_store_temperature_task():
    city = settings.CITY_TO_TRACK
    if not city:
        return "CITY_TO_TRACK env variable is not set"

    temperature, timezone_offset = fetch_city_temperature(city)

    if temperature is not None and timezone_offset is not None:
        TemperatureRecord.objects.create(
            city=city, temperature=temperature, timezone_offset=timezone_offset
        )
        logger.info(f"Stored temperature for {city} {temperature}°C")
        return f"Stored temperature for {city} {temperature}°C"
    else:
        logger.error(f"Failed to fetch temperature for {city}")
        return f"Failed to fetch temperature for {city}"
