from rest_framework.serializers import ModelSerializer, SerializerMethodField
from weather_tracker.models import TemperatureRecord
from datetime import timedelta, timezone


class TemperatureRecordSerializer(ModelSerializer):
    local_time = SerializerMethodField()

    class Meta:
        model = TemperatureRecord
        fields = ['city', 'temperature', 'local_time']

    def get_local_time(self, obj):
        tz_offset = timezone(timedelta(seconds=obj.timezone_offset))
        return obj.time_recorded.astimezone(tz_offset).strftime('%Y-%m-%d %H:%M:%S')
