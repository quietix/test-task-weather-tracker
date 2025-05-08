from django.http import HttpResponse
from django.conf import settings

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from weather_tracker.models import TemperatureRecord
from weather_tracker.serializers import TemperatureRecordSerializer


def index(request):
    return HttpResponse("Hello")


class WeatherStatisticsView(APIView):
    http_method_names = ("get",)

    def get(self, request):
        city = settings.CITY_TO_TRACK
        if not city: raise APIException(detail="Couldn't fetch env data", code=500)

        temperature_records = TemperatureRecord.objects.filter(city=city)
        return Response(TemperatureRecordSerializer(temperature_records, many=True).data)
