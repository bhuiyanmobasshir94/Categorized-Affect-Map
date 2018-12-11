from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

FAMILIARITY_CHOICE = [(1,'For the first time'),(2,'More Often')]
ACCOMPANY_CHOICE = [(1,'Alone'),(2,'With family member(s)'),(3,'With friend(s)'),(4,'With adult(s)'),(5,'with child(ren)')]
COMFORTABILITY_CHOICE = [(1,'Very uncomfortable'),(2,'Uncomfortable'),(3,'Slightly uncomfortable'),(4,'Neutral'),(5,'Slightly comfortable'),(6,'Comfortable'),(7,'Very comfortable')]

from classification.models import Category,Feature
from place.models import Location

from multiselectfield import MultiSelectField

features = Feature.objects.filter(status=1)

FEATURES_CHOICE = list((x.id, x.name) for x in features)


class AffectiveResponse(models.Model):
    class Meta:
        verbose_name_plural = "affective responses"
    location = models.ForeignKey(Location,on_delete=models.CASCADE,null=True)#
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    familiarity = models.IntegerField(choices=FAMILIARITY_CHOICE,blank=False)
    accompany = models.IntegerField(choices=ACCOMPANY_CHOICE,blank=False)
    feature_set =  MultiSelectField(choices=FEATURES_CHOICE,min_choices=5,max_choices=5,max_length=20,default=0)
    comfortability = models.IntegerField(choices=COMFORTABILITY_CHOICE,blank=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.location.name + "_" + str(self.category.name)
