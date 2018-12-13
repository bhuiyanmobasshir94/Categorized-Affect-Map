import os
import pandas as pd
import numpy as np
import random
import django
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

locations = Location.objects.all()
for location in locations:
    master_sets = location.master_set.all()
    cat_list= set([])
    loc_dict = dict()
    for master in master_sets:
        cat_list.add(master.category.name)
        if master.category.name in cat_list:
            master.feature_set.filter(category=master.category) 