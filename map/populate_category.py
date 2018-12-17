import os
import pandas as pd
import numpy as np
import random
import django
import folium
import branca
from django.utils import timezone
from django.conf import settings

import sys
sys.path.append("..")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'categorized_affect_map.settings')
django.setup()

from classification.models import Category, Feature
from place.models import Area, Location
from response.models import AffectiveResponse
from forecast.models import Weather
from map.models import Master

FAMILIARITY_CHOICE = [(1,'For the first time'),(2,'More Often')]
ACCOMPANY_CHOICE = [(1,'Alone'),(2,'With family member(s)'),(3,'With friend(s)'),(4,'With adult(s)'),(5,'With child(ren)')]
COMFORTABILITY_CHOICE = [(1,'Very uncomfortable'),(2,'Uncomfortable'),(3,'Slightly uncomfortable'),(4,'Neutral'),(5,'Slightly comfortable'),(6,'Comfortable'),(7,'Very comfortable')]


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
            <div class="card">
                <div class="card-content cyan lighten-4">
                <div class="row">
                    <div class="col s6 blue lighten-5"><h6>Area: """+str(response_list[2])+"""</h6></div>
                    <div class="col s6 blue lighten-4"><h6>Location: """+str(response_list[3])+"""</h6></div>
                    <div class="col s6 blue lighten-4"><h6>Category: """+str(response_list[4])+"""</h6></div>
                    <div class="col s6 blue lighten-5"><h6>Total Submission: """+str(response_list[5])+"""</h6></div>
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


        iframe = branca.element.IFrame(html=html,width=410,height=310)
        popup = folium.Popup(iframe,parse_html=True)
        folium.Marker([raw[0],raw[1]],popup=popup,icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
    m.save('./templates/map/category.html')
