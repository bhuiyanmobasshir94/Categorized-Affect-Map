from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import Context, loader
from django.views.decorators.clickjacking import xframe_options_sameorigin
import json
import requests
# Create your views here.

from classification.models import Category, Feature
from place.models import Area, Location
from response.models import AffectiveResponse
from forecast.models import Weather
from .models import Master

def get_weather(latitude_,longitude_):
    latitude = latitude_
    longitude = longitude_
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=8f47bbfcc82517d109015de292ab80cd&units=metric'.format(latitude, longitude)
    res = requests.get(url)
    data = res.json()
    response = dict(main=data['weather'][0]['main'],desc=data['weather'][0]['description'],temp=data['main']['temp'],pressure=data['main']['pressure'],humidity=data['main']['humidity'],temp_min=data['main']['temp_min'],temp_max=data['main']['temp_max'],wind_speed=data['wind']['speed'],wind_degree=data['wind']['deg'],datetime=data['dt'],clouds_all=data['clouds']['all'],sys_sunrise=data['sys']['sunrise'],sys_sunset=data['sys']['sunset'])
    return response

def submit_response(request):
    place_name = request.POST.get('Location.Place', None)#
    latitude = request.POST.get('Location.Latitude', None)#
    longitude = request.POST.get('Location.Longitude', None)#
    area = request.POST.get('Area', None)#
    category = request.POST.get('Category', None)#
    feature = request.POST.get('Feature', None)##
    familiarity = request.POST.get('Familiarity', None)#
    accompany = request.POST.get('Accompany', None)#
    comfortability = request.POST.get('Comfortability', None)#
    area_status = request.POST.get('Area.status', None)#
    feature_string = request.POST.get('feature_string', None)
    feature_list = feature_string.split(',')[:-1]
    
    if int(area_status) == 1:
        weather_res = get_weather(float(latitude),float(longitude))
        a = Area.objects.get(pk=int(area))
        c = Category.objects.get(pk=int(category))
        f = c.feature_set.all()
        l = a.location_set.create(name=str(place_name),latitude=float(latitude),longitude=float(longitude),pub_date=timezone.now())
        a.save()
        w = l.weather_set.create(main=weather_res['main'],desc=weather_res['desc'],temp=weather_res['temp'],pressure=weather_res['pressure'],humidity=weather_res['humidity'],temp_min=weather_res['temp_min'],temp_max=weather_res['temp_max'],wind_speed=weather_res['wind_speed'],wind_degree=weather_res['wind_degree'],datetime=weather_res['datetime'],clouds_all=weather_res['clouds_all'],sys_sunrise=weather_res['sys_sunrise'],sys_sunset=weather_res['sys_sunset'],pub_date=timezone.now())
        ar = l.affectiveresponse_set.create(category=c,familiarity=int(familiarity),accompany=int(accompany),comfortability=int(comfortability),pub_date=timezone.now())
        batch_id = m = Master.objects.order_by('-pub_date')[0].batch_id
        b_id = batch_id+1
        for f_t in feature_list:
            temp_f = c.feature_set.get(pk=int(f_t))
            m = l.master_set.create(area=a,category=c,feature=temp_f,weather=w,response=ar,latitude=latitude,longitude=longitude,batch_id=b_id,pub_date=timezone.now())
        l.save()
        print(l)
        return HttpResponseRedirect(reverse('map:index'))
    else:
        print("Escaped Save")
        return HttpResponseRedirect(reverse('map:index'))


def index(request):
    area_list = Area.objects.filter(status=1).order_by('-pub_date')
    category_list = Category.objects.filter(status=1).order_by('-pub_date')
    context = {
        'latest_area_list': area_list,
        'latest_category_list': category_list,
    }
    return render(request,'map/index.html',context)

def get_features(request):
    id = request.GET.get('id','')
    cat = Category.objects.get(pk=id) 
    result = list(Feature.objects.filter(category=cat).values('id', 'name')) 
    return HttpResponse(json.dumps(result), content_type="application/json") 

def get_area(request):
    id = request.GET.get('id','')
    area = Area.objects.get(pk=id) 
    result = list(Area.objects.filter(name=area).values('top_north_lat_TP','left_west_long_TL','right_east_long_TP','bottom_south_lat_TL')) 
    return HttpResponse(json.dumps(result), content_type="application/json") 

def map_view(request):
    area_list = Area.objects.filter(status=1).order_by('-pub_date')
    category_list = Category.objects.filter(status=1).order_by('-pub_date')
    area_res = request.POST.get('Area', False)
    category_res = request.POST.get('Category', False)
    if area_res == False and category_res == False:
        context = {
        'latest_area_list': area_list,
        'latest_category_list': category_list,
        }
    else:
        area = get_object_or_404(Area, pk=area_res)
        category = get_object_or_404(Category, pk=category_res)
        context = {
        'latest_area_list': area_list,
        'latest_category_list': category_list,
        'area_targeted': area,
        'category_targeted': category,
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