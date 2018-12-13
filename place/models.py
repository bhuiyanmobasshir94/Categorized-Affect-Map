from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

class Area(models.Model):
    class Meta:
        verbose_name_plural = "areas"
    name = models.CharField(max_length=200)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    top_north_lat_TP = models.FloatField(default=0.0)
    left_west_long_TL = models.FloatField(default=0.0)
    right_east_long_TP = models.FloatField(default=0.0)
    bottom_south_lat_TL = models.FloatField(default=0.0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

class Location(models.Model):
    class Meta:
        verbose_name_plural = "Locations"
    area = models.ForeignKey(Area,on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name