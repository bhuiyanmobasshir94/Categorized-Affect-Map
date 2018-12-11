from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

from classification.models import Category,Feature
from place.models import Location,Area
from forecast.models import Weather
from response.models import AffectiveResponse


class Master(models.Model):
    class Meta:
        verbose_name_plural = "master model"
    area = models.ForeignKey(Area,on_delete=models.CASCADE,null=True)
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,null=True)
    weather = models.ForeignKey(Weather,on_delete=models.CASCADE,null=True)
    response = models.ForeignKey(AffectiveResponse,on_delete=models.CASCADE,null=True)

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.area.name + "_" + str(self.latitude) + "_" + str(self.longitude)