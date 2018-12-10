import os
import pandas as pd
import numpy as np
import random
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'categorized_affect_map.settings')
django.setup()
from classification.models import Category, Feature
from django.utils import timezone

category_list = ['socialBehaviour.xlsx','Activity.xlsx','Transportation.xlsx']
cat_name = ["Social Behavior","Activities","Transportation"]
i=0
for file_name in category_list:
    excel_file = 'data/{}'.format(file_name)
    data = pd.read_excel(excel_file)
    df_data = pd.DataFrame(data)
    df_data['Feature'].apply(lambda x:str(x))
    df_data['Value'].apply(lambda x:int(x))
    df_data['Importance'].apply(lambda x:int(x))

    # data = [df_data[df_data['Feature']==df_data['Feature'].unique()[i]][['Feature','Value','Importance']].values.tolist() for i in range(len(df_data['Feature'].unique()))]

    c = Category.objects.get(name=cat_name[i])

    for index,row in df_data.iterrows():
        c.feature_set.create(name=row['Feature'],status=1,value=row['Value'],priority=row['Importance'],votes=random.randint(1,120),pub_date=timezone.now())

    c.save()
    i+=1
