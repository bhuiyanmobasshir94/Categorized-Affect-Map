import requests

def get_weather(latitude_,longitude_):
    latitude = latitude_
    longitude = longitude_
    url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=8f47bbfcc82517d109015de292ab80cd&units=metric'.format(latitude, longitude)
    res = requests.get(url)
    data = res.json()
    response = dict(main=data['weather'][0]['main'],desc=data['weather'][0]['description'],temp=data['main']['temp'],pressure=data['main']['pressure'],humidity=data['main']['humidity'],temp_min=data['main']['temp_min'],temp_max=data['main']['temp_max'],wind_speed=data['wind']['speed'],wind_degree=data['wind']['deg'],datetime=data['dt'],clouds_all=data['clouds']['all'],sys_sunrise=data['sys']['sunrise'],sys_sunset=data['sys']['sunset'])
    return response
    


# def show_data(data):
#     temp = data['main']['temp']
#     wind_speed = data['wind']['speed']
#     latitude = data['coord']['lat']
#     longitude = data['coord']['lon']
#     description = data['weather'][0]['description']


def get_location(latitude_,longitude_):
    latitude = latitude_
    longitude = longitude_
    url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=1'.format(float(latitude),float(longitude))
    res = requests.get(url)
    data = res.json()
    return data["display_name"]

# value = get_location(23.8197,90.4349)
# value["display_name"]