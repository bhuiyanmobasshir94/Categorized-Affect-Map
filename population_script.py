import os
import pandas as pd
import numpy as np
import random
import django
from django.utils import timezone
from populate_weather import get_location,get_weather

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'categorized_affect_map.settings')
django.setup()

from classification.models import Category, Feature
from place.models import Area, Location
from response.models import AffectiveResponse
from forecast.models import Weather
from map.models import Master

cat_name_list = ["Social Behavior","Activities","Transportation"]

excel_file = 'data/new-lat-And-long.xlsx'
data = pd.read_excel(excel_file)
df_data = pd.DataFrame(data)
df_data['lon'].fillna(90.43, inplace=True)
df_data['lat'].fillna(23.82, inplace=True)
df_data['month'].fillna(12, inplace=True)
df_data['lat'].apply(lambda x:float(x))
df_data['lon'].apply(lambda x:float(x))

b_id = 1

for cat_name in cat_name_list:
    loop = random.randint(110,155)
    c = Category.objects.get(name=cat_name)
    f = c.feature_set.all() #f[0].id
    f_count = c.feature_set.count()
    a = Area.objects.get(name="Bashundhara")

    for index,row in df_data.iterrows():
        f_list = list()
        for i in range(5):
            rn = random.randint(1,f_count)
            if rn not in f_list:
                f_list.append(rn)
            else:
                rn = random.randint(1,f_count)
                f_list.append(rn)
        name_res = get_location(row['lat'],row['lon'])
        weather_res = get_weather(row['lat'],row['lon'])
        l = a.location_set.create(name=name_res,latitude=row['lat'],longitude=row['lon'],pub_date=timezone.now())
        w = l.weather_set.create(main=weather_res['main'],desc=weather_res['desc'],temp=weather_res['temp'],pressure=weather_res['pressure'],humidity=weather_res['humidity'],temp_min=weather_res['temp_min'],temp_max=weather_res['temp_max'],wind_speed=weather_res['wind_speed'],wind_degree=weather_res['wind_degree'],datetime=weather_res['datetime'],clouds_all=weather_res['clouds_all'],sys_sunrise=weather_res['sys_sunrise'],sys_sunset=weather_res['sys_sunset'],pub_date=timezone.now())
        ar = l.affectiveresponse_set.create(category=c,familiarity=random.randint(1,2),accompany=random.randint(1,5),comfortability=random.randint(1,7),pub_date=timezone.now())
        for f_t in f_list:
            n = f_t - 1
            temp_f = f[n]
            m = l.master_set.create(area=a,category=c,feature=temp_f,weather=w,response=ar,latitude=row['lat'],longitude=row['lon'],batch_id=b_id,pub_date=timezone.now())
        b_id +=1
        l.save()
        if loop and (index+1) == loop:
            break
    a.save()