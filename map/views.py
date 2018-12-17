from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.template import Context, loader
from django.views.decorators.clickjacking import xframe_options_sameorigin
import json
import requests
import folium
import branca
import os
import pandas as pd
import numpy as np
import random
import time
# Create your views here.

from classification.models import Category, Feature
from place.models import Area, Location
from response.models import AffectiveResponse
from forecast.models import Weather
from .models import Master

FAMILIARITY_CHOICE = [(1,'For the first time'),(2,'More Often')]
ACCOMPANY_CHOICE = [(1,'Alone'),(2,'With family member(s)'),(3,'With friend(s)'),(4,'With adult(s)'),(5,'With child(ren)')]
COMFORTABILITY_CHOICE = [(1,'Very uncomfortable'),(2,'Uncomfortable'),(3,'Slightly uncomfortable'),(4,'Neutral'),(5,'Slightly comfortable'),(6,'Comfortable'),(7,'Very comfortable')]

##________________________________________________##

def generate_html(response_list):

    html = """

    <!DOCTYPE html>
        <html>
        <head>
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
            <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
            <style type="text/css">
            *{
                padding: 0;
                margin: 0;
            }
            body{
                padding: 0;
                margin: 0;
            }
            .card{
                margin: initial !important;
            }
            .card-content h6{
                color: #0d47a1;
            }
            </style>
        </head>
        <body>
             <div class="row">
                    <div class="col s12">
            <div class="card">
                <div class="card-content cyan lighten-4">
                <div class="row">
                    <div class="col s12 blue lighten-5"><h6>Area: """+str(response_list[2])+"""</h6></div>
                    <div class="col s12 blue lighten-4"><h6>Location: """+str(response_list[3])+"""</h6></div>
                    <div class="col s12 blue lighten-5"><h6>Category: """+str(response_list[4])+"""</h6></div>
                    <div class="col s12 blue lighten-4"><h6>Total Submission: """+str(response_list[5])+"""</h6></div>
                </div>
                </div>
                <div class="card-tabs">
                <ul class="tabs tabs-fixed-width">
                    <li class="tab"><a class="active" href="#test4">Feature</a></li>
                    <li class="tab"><a href="#test5">Familiarity</a></li>
                    <li class="tab"><a href="#test6">Accompany</a></li>
                    <li class="tab"><a href="#test7">Comfort Level</a></li>
                    <li class="tab"><a href="#test8">Weather</a></li>
                </ul>
                </div>
                <div class="card-content cyan lighten-4">
                <div id="test4">"""
    for k,v in response_list[6].items():
        html+="""

            <div class="row">
              <div class="col s6 blue lighten-5"><h6>{}</h6></div>
              <div class="col s6 blue lighten-4"><h6>{}%</h6></div>
            </div>

              """.format(k,v)            
    
    html+=    """</div>
                <div id="test5">"""
    
    for k,v in response_list[7].items():
        html+="""

            <div class="row">
              <div class="col s6 blue lighten-5"><h6>{}</h6></div>
              <div class="col s6 blue lighten-4"><h6>{}%</h6></div>
            </div>

            """.format(k,v)     
    
    html+=  """</div>
                <div id="test6">"""

    for k,v in response_list[8].items():
        html+="""

            <div class="row">
              <div class="col s6 blue lighten-5"><h6>{}</h6></div>
              <div class="col s6 blue lighten-4"><h6>{}%</h6></div>
            </div>

            """.format(k,v)    

    html+=  """</div>
                <div id="test7">"""
    
    
    for k,v in response_list[9].items():
        html+="""

            <div class="row">
              <div class="col s6 blue lighten-5"><h6>{}</h6></div>
              <div class="col s6 blue lighten-4"><h6>{}%</h6></div>
            </div>

            """.format(k,v) 
    
    
    html+=  """</div>
                <div id="test8">"""

    for k,v in response_list[10].items():
        html+="""

            <div class="row">
              <div class="col s6 blue lighten-5"><h6>{}</h6></div>
              <div class="col s6 blue lighten-4"><h6>{}</h6></div>
            </div>

            """.format(k,v)

    html+=  """</div>
                </div>
            </div>
            </div>
            </div>
            <script src="https://code.jquery.com/jquery-3.3.1.min.js" integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            <script type="text/javascript">
                $(document).ready(function(){
                $('.tabs').tabs();
                });
            </script>
        </body>
        </html>


            """
    return html


def generate_category_html(area_id,cat_id):
    area = Area.objects.get(pk=int(area_id)) ## Area selected
    category = Category.objects.get(pk=int(cat_id)) ## Category selected
    m = folium.Map(location=[area.latitude,area.longitude],zoom_start=15,min_zoom=5)
    locations = area.location_set.filter(affectiveresponse__category=category)  ## A set or list of locations for that particular area and category
    for location in locations:
        location_name = location.name
        year = location.pub_date.year
        month = location.pub_date.month
        day = location.pub_date.day
        total_feature_count = location.master_set.filter(category=category).count() ## Total feature submitted for this particular location
        total_affective_response_submit = location.affectiveresponse_set.filter(category=category).count() ## Total affective response submitted for this particular location
        location_feature_set = list(location.master_set.filter(category=category))
        location_weather_set = set([(lambda x: x.weather)(x) for x in location_feature_set])
        location_feature_set = set([(lambda x: x.feature)(x) for x in location_feature_set])

        temp_mean = np.mean([(lambda x: x.temp)(x) for x in location_weather_set])
        pressure_mean = np.mean([(lambda x: x.pressure)(x) for x in location_weather_set])
        humidity_mean = np.mean([(lambda x: x.humidity)(x) for x in location_weather_set])
        temp_min_mean = np.mean([(lambda x: x.temp_min)(x) for x in location_weather_set])
        temp_max_mean = np.mean([(lambda x: x.temp_max)(x) for x in location_weather_set])
        wind_speed_mean = np.mean([(lambda x: x.wind_speed)(x) for x in location_weather_set])

        location_weather_dict = dict()
        location_weather_dict['Mean temperature'] = temp_mean
        location_weather_dict['Mean pressure'] = pressure_mean 
        location_weather_dict['Mean humidity'] = humidity_mean
        location_weather_dict['Mean minimum temperature'] = temp_min_mean
        location_weather_dict['Mean maximum temperature'] = temp_max_mean
        location_weather_dict['Mean wind speed'] = wind_speed_mean
        
        location_feature_dict = dict()
        for feature in location_feature_set:
            temp_feature_count = location.master_set.filter(feature=feature.id).count()
            temp_feature_percentage = float((temp_feature_count/total_feature_count)*100)
            location_feature_dict[feature.name] = temp_feature_percentage
        
        location_familiarity_dict = dict()
        for val in FAMILIARITY_CHOICE:
            temp_l_f_c = location.affectiveresponse_set.filter(familiarity=int(val[0]),category=category).count()
            temp_l_f_percentage = float((temp_l_f_c/total_affective_response_submit)*100)
            location_familiarity_dict[val[1]] = temp_l_f_percentage
        
        location_accompany_dict = dict()
        for val in ACCOMPANY_CHOICE:
            temp_l_f_c = location.affectiveresponse_set.filter(accompany=int(val[0]),category=category).count()
            temp_l_f_percentage = float((temp_l_f_c/total_affective_response_submit)*100)
            location_accompany_dict[val[1]] = temp_l_f_percentage

        location_comfortability_dict = dict()
        for val in COMFORTABILITY_CHOICE:
            temp_l_f_c = location.affectiveresponse_set.filter(comfortability=int(val[0]),category=category).count()
            temp_l_f_percentage = float((temp_l_f_c/total_affective_response_submit)*100)
            location_comfortability_dict[val[1]] = temp_l_f_percentage

        raw = [location.latitude, location.longitude, area.name, location_name, category.name, total_affective_response_submit, location_feature_dict, location_familiarity_dict, location_accompany_dict, location_comfortability_dict, location_weather_dict, year, month, day]
        html = generate_html(raw)

        iframe = branca.element.IFrame(html=html,width=290,height=300)
        popup = folium.Popup(iframe,parse_html=True)
        folium.Marker([raw[0],raw[1]],popup=popup,icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

    m.save(os.path.join(os.path.dirname(__file__), 'templates/map/category.html'))


###________________________________________________###





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
        generate_category_html(area.id,category.id)
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