from django.db import models


class CO2rate(models.Model):
    timestamp = models.DateTimeField()
    co2_rate = models.FloatField(default=0.0)
