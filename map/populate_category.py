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

categories = Category.objects.all()
locations = Location.objects.all()
for location in locations:
    master_sets = location.master_set.all()
    master_sets_count = location.master_set.count()
    for category in categories:
        category_master_sets = location.master_set.filter(category=category)
    for master in master_sets:
        