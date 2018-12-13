from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import Context, loader
from django.views.decorators.clickjacking import xframe_options_sameorigin

# Create your views here.

from classification.models import Category, Feature
from place.models import Area, Location
from response.models import AffectiveResponse
from forecast.models import Weather
from .models import Master

def index(request):
    context = {
    }
    return render(request,'map/index.html',context)

def map_view(request):
    
    context = {
    }
    return render(request,'map/map_view.html',context)

@xframe_options_sameorigin
def category(request):
    template = loader.get_template("map/category.html")
    return HttpResponse(template.render())

def about(request):
    # context = {
    # }
    # return render(request,'map/index.html',context)
    return HttpResponse("Hello to about")