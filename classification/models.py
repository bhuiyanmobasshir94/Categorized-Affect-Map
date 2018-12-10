from django.db import models
from django.utils import timezone
import datetime

# Create your models here.

CHOICE = [(1,'Active'),(0,'Inactive')]

class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"
    name = models.CharField(max_length=100)
    status = models.BooleanField(choices=CHOICE,default=0,blank=False)
    priority = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name

class Feature(models.Model):
    class Meta:
        verbose_name_plural = "features"
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.BooleanField(choices=CHOICE,default=0,blank=False)
    value = models.IntegerField(default=0)
    priority = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.name