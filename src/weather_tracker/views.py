from datetime import timezone, timedelta, datetime

from django.conf import settings
from django.utils.dateparse import parse_date

from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.views import APIView

from weather_tracker.models import TemperatureRecord
from weather_tracker.serializers import TemperatureRecordSerializer
from weather_tracker.exceptions import InvalidTokenException, InvalidDateFormat


class WeatherStatisticsView(APIView):
    http_method_names = ("get",)

    def check_token(self, request):
        x_token = request.headers.get('x-token')

        if not x_token or len(x_token) != 32:
            raise InvalidTokenException()


    def get(self, request, date: str):
        self.check_token(request)

        parsed_date = parse_date(date)
        if not parsed_date:
            raise InvalidDateFormat

        city = settings.CITY_TO_TRACK
        if not city:
            raise APIException(detail="Couldn't fetch env data")

        first_record = TemperatureRecord.objects.filter(city=city).first()
        if not first_record:
            return Response([])

        tz_offset = timezone(timedelta(seconds=first_record.timezone_offset))

        local_start = datetime.combine(parsed_date, datetime.min.time(), tz_offset)
        local_end = local_start + timedelta(days=1)

        utc_start = local_start.astimezone(timezone.utc)
        utc_end = local_end.astimezone(timezone.utc)

        temperature_records = TemperatureRecord.objects.filter(
            city=city,
            time_recorded__gte=utc_start,
            time_recorded__lt=utc_end
        )

        return Response(TemperatureRecordSerializer(temperature_records, many=True).data)
