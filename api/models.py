from django.db import models
from django.contrib.gis.db import models


class Observation(models.Model):
    observationId = models.IntegerField(primary_key=True)
    datetime = models.DateTimeField()
    geom = models.GeometryField()
    altGPS = models.FloatField(default=0.0)
    temp = models.FloatField(default=0.0)
    hum = models.FloatField(default=0.0)
    altBar = models.FloatField(default=0.0)
    pressure = models.FloatField(default=0.0)
    NO2 = models.FloatField(default=0.0)
    CO = models.FloatField(default=0.0)
    NH3 = models.FloatField(default=0.0)
    PM1_0 = models.FloatField(default=0.0)
    PM2_5 = models.FloatField(default=0.0)
    PM10_0 = models.FloatField(default=0.0)



