import folium
import pandas as pd
import numpy as np
import time
import folium.plugins as plugins

excel_file = 'new-lat-and-long.xlsx'
data = pd.read_excel(excel_file)
df_data = pd.DataFrame(data)
df_data['lon'].fillna(90.43, inplace=True)
df_data['month'].fillna(12, inplace=True)
df_data['lat'].apply(lambda x:float(x))
df_data['lon'].apply(lambda x:float(x))


data = [df_data[df_data['month']==df_data['month'].unique()[i]][['lat','lon']].values.tolist() 
        for i in range(len(df_data['month'].unique()))]

monthDict = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 
            7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
index = [monthDict[i] for i in sorted(df_data['month'].unique())]

# df_data.isnull().sum()

# df_data['lat'].str.extract('(\d*\.?\d*)', expand=False)
# df_data['lon'].str.extract('(\d*\.?\d*)', expand=False)
# for i in range(0,len(df_data)):
#     df_data = df_data[ df_data['lat'].str.extract('(\d*\.?\d*)', expand=False).astype(float)]
#     df_data = df_data[ df_data['lon'].str.extract('(\d*\.?\d*)', expand=False).astype(float)]
# df_data['month'] = 'Dec'





# index = [monthDict[i] for i in sorted(df_data['month'].unique())]
# index=[12]

m = folium.Map(
    location=[23.8196,90.4415],
    zoom_start=12
)

hm = plugins.HeatMapWithTime(data=data,index=index)
hm.add_to(m)

# m.add_child(folium.LatLngPopup())
m.save("heatmap.html")