from django.db import models


class TemperatureRecord(models.Model):
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    time_recorded = models.DateTimeField(auto_now_add=True)
    timezone_offset = models.IntegerField(default=0)

    def __str__(self):
        return (f"{self.city} at "
                f"{self.time_recorded.strftime('%Y-%m-%d %H:%M')} = {self.temperature}°C")

    class Meta:
        ordering = ['-time_recorded']
