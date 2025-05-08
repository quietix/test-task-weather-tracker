from django.urls import path
from weather_tracker.views import index, WeatherStatisticsView


urlpatterns = [
    path("", index, name="index"),
    path("statistics/<str:date>", WeatherStatisticsView.as_view(), name="get-weather-statistics"),
]
