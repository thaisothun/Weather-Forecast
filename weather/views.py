from django.shortcuts import render
import requests
import datetime
import json
from ipware import get_client_ip


# Create your views here.

def get_weather(city):
    api_key = '0d1f871ccf6aae7ab1fa7fa87ae21a1a'
    current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    current_data = requests.get(current_url).json()
    forecast_url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&exclude=current,minutely,hourly,alerts&appid={api_key}'
    forecast_data = requests.get(forecast_url).json()
    if current_data['cod'] == 200 and forecast_data['cod'] == '200':  
        
        current_weather = {
            'city': current_data['name'],
            'country' : current_data['sys']['country'],
            'temp' : current_data['main']['temp'],
            'temp_min' : current_data['main']['temp_min'],
            'temp_max' : current_data['main']['temp_max'],
            'wind_speed' : current_data['wind']['speed'],
            'weather' : current_data['weather'][0]['main'],
            'weather_des' : current_data['weather'][0]['description'],
            'weather_icon' : current_data['weather'][0]['icon'],
            'sunrise' : datetime.datetime.fromtimestamp(current_data['sys']['sunrise']).strftime("%I:%M:%S %p"),
            'sunset' : datetime.datetime.fromtimestamp(current_data['sys']['sunset']).strftime("%I:%M:%S %p")
        }
        
        forecast_weather = []
        for data in forecast_data['list'][:40:8]:
            forecast_weather.append({
            'date': datetime.datetime.fromtimestamp(data['dt']).strftime("%A %B %d, %Y"),
            'temp' : data['main']['temp'],
            'temp_min' : data['main']['temp_min'],
            'temp_max' : data['main']['temp_max'],
            'wind_speed' : data['wind']['speed'],
            'weather' : data['weather'][0]['main'],
            'weather_des' : data['weather'][0]['description'],
            'weather_icon' : data['weather'][0]['icon'],
            })  
        
        return current_weather, forecast_weather

    else:
        pass        

def current_city(request):
    ip_address = get_client_ip(request)
    location_url = f"https://iplocate.io/api/lookup/{ip_address['ip']}?apikey=444e70c687d6334254a9a997e1ccacab"
    location = requests.get(location_url).json()
    current_city = location['city']
    city1 = request.POST.get('city1','NA')
    city2 = request.POST.get('city2','NA')
    city3 = request.POST.get('city3','NA')
    print(city1)
    current_weather, forecast_weather = get_weather(city=current_city)
    try:
        current_weather_city1, forecast_weather_city1 = get_weather(city1)
    except:
        current_weather_city1, forecast_weather_city1 = None, None    
    try:
        current_weather_city2, forecast_weather_city2 = get_weather(city2)
    except:
        current_weather_city2, forecast_weather_city2 = None, None
    try:
        current_weather_city3, forecast_weather_city3 = get_weather(city3)
    except:
        current_weather_city3, forecast_weather_city3 = None, None

    context = {
        'current_weather': current_weather,
        'forecast_weather': forecast_weather,
        'current_weather_city1': current_weather_city1,
        'forecast_weather_city1': forecast_weather_city1,
        'current_weather_city2': current_weather_city2,
        'forecast_weather_city2': forecast_weather_city2,
        'current_weather_city3': current_weather_city3,
        'forecast_weather_city3': forecast_weather_city3,    
    }

    return render(request,'weather_app/index.html', context)

def home(request):
    ip_address = requests.get('https://api.iplocate.io/json').json()
    location_url = f"https://iplocate.io/api/lookup/{ip_address['ip']}?apikey=444e70c687d6334254a9a997e1ccacab"
    location = requests.get(location_url).json()
    current_city = location['city']
    current_weather, forecast_weather = get_weather(city=current_city)
    context = {
        'current_weather': current_weather,
        'forecast_weather': forecast_weather,
    }

    return render(request,'weather_app/home.html', context)
