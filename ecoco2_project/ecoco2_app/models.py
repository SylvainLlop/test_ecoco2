from django.db import models
import datetime


class CO2rate(models.Model):
    timestamp = models.DateTimeField()
    co2_rate = models.FloatField(default=0.0)

    def __str__(self):
        return_str = datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        return return_str


class LowFrequencyCO2rate(models.Model):
    timestamp = models.DateTimeField()
    co2_rate = models.FloatField(default=0.0)

    def __str__(self):
        return_str = datetime.datetime.strftime(self.timestamp, "%Y-%m-%d %H:%M:%S")
        return return_str
