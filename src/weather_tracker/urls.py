from django.urls import path
from weather_tracker.views import WeatherStatisticsView


urlpatterns = [
    path("statistics/<str:date>", WeatherStatisticsView.as_view(), name="get-weather-statistics"),
]
