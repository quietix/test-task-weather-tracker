import pytest
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from weather_tracker.models import TemperatureRecord


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def valid_token() -> str:
    return "a" * 32


@pytest.fixture
def city_name() -> str:
    settings.CITY_TO_TRACK = "TestCity"
    return settings.CITY_TO_TRACK


@pytest.fixture
def temperature_record(city_name) -> TemperatureRecord:
    record = TemperatureRecord.objects.create(
        city=city_name,
        temperature=133.333,
        timezone_offset=3600
    )
    return record


@pytest.fixture
def date_str(temperature_record):
    return temperature_record.time_recorded.date().isoformat()


@pytest.mark.django_db
def test_valid_request_returns_data(api_client, valid_token, temperature_record, date_str):
    url = reverse("get-weather-statistics", kwargs={'date': date_str})
    response = api_client.get(url, HTTP_X_TOKEN=valid_token)

    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) >= 1
    assert response.data[0]["temperature"] == temperature_record.temperature


@pytest.mark.django_db
def test_missing_token(api_client, date_str):
    url = reverse("get-weather-statistics", kwargs={'date': date_str})
    response = api_client.get(url)

    assert response.status_code == 400
    assert "Invalid x-token" in str(response.data)


@pytest.mark.django_db
def test_invalid_token_length(api_client, date_str):
    url = reverse("get-weather-statistics", kwargs={'date': date_str})
    response = api_client.get(url, HTTP_X_TOKEN="short-token")

    assert response.status_code == 400
    assert "Invalid x-token" in str(response.data)


@pytest.mark.django_db
def test_invalid_date_format(api_client, valid_token):
    url = reverse("get-weather-statistics", kwargs={'date': 'invalid-date'})
    response = api_client.get(url, HTTP_X_TOKEN=valid_token)

    assert response.status_code == 400
    assert "Invalid date format" in str(response.data)


@pytest.mark.django_db
def test_no_temperature_records(api_client, valid_token):
    date_with_no_record = '1111-11-11'
    url = reverse("get-weather-statistics", kwargs={'date': date_with_no_record})
    response = api_client.get(url, HTTP_X_TOKEN=valid_token)

    assert response.status_code == 200
    assert response.data == []
