from django.db import models

# Create your models here.

class TemperatureReading(models.Model):
    timestamp = models.DateTimeField(unique=True)
    temperature = models.FloatField()
    relative_humidity = models.IntegerField()
    absolute_humidity = models.FloatField()
    dew_point = models.FloatField()
    vapor_pressure_deficit = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.temperature}C, {self.relative_humidity}%"