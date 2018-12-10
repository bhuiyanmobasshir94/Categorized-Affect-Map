from django.db import models
from django.utils import timezone
import datetime

# Create your models here.
from place.models import Location

class Weather(models.Model):
    class Meta:
        verbose_name_plural = "weathers"
    location = models.ForeignKey(Location,on_delete=models.CASCADE)
    main = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    temp = models.FloatField(default=0.0)
    pressure = models.IntegerField(default=0)
    humidity = models.IntegerField(default=0)
    temp_min = models.FloatField(default=0.0)
    temp_max = models.FloatField(default=0.0)
    wind_speed = models.IntegerField(default=0)
    wind_degree = models.IntegerField(default=0)
    datetime = models.IntegerField(default=0)
    clouds_all = models.IntegerField(default=0)
    sys_sunrise = models.IntegerField(default=0)
    sys_sunset = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.location.name + "_" + str(self.datetime)