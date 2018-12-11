import requests

def get_weather(latitude_,longitude_):
    # latitude = latitude_
    # longitude = longitude_
    # url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid=8f47bbfcc82517d109015de292ab80cd&units=metric'.format(latitude, longitude)
    # res = requests.get(url)
    # data = res.json()
    response = dict(main="Haze",desc="haze",temp=18,pressure=1014,humidity=72,temp_min=18,temp_max=18,wind_speed=1.5,wind_degree=310,datetime=1544556600,clouds_all=20,sys_sunrise=1544488256,sys_sunset=1544526753)
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
    url = 'https://nominatim.openstreetmap.org/reverse?format=json&lat={}&lon={}&zoom=18&addressdetails=1'.format(latitude, longitude)
    res = requests.get(url)
    data = res.json()
    return data["display_name"]

# value = get_location(23.8197,90.4349)
# value["display_name"]