from django.shortcuts import render
import requests
import base64
import json

def index(request):
    weather_info = None
    search_history = []
    last_city = request.COOKIES.get('last_city')
    if last_city:
        last_city = base64.b64decode(last_city).decode('utf-8')

    search_history_cookie = request.COOKIES.get('search_history')
    if search_history_cookie:
        search_history = json.loads(base64.b64decode(search_history_cookie).decode('utf-8'))

    if 'city' in request.GET:
        city = request.GET['city']
        headers = {'Accept-Language': 'ru'}
        response = requests.get(f'https://wttr.in/{city}?format=j2', headers=headers)
        if response.status_code == 200:
            data = response.json()
            response = requests.get(f'https://wttr.in/{city}?format=1', headers=headers)
            emoji_data = response.text.split()
            emoji = emoji_data[0]
            current_condition = data['current_condition'][0]
            nearest_area = data['nearest_area'][0]
            weather_info = {
                'emoji': emoji,
                'country': nearest_area['country'][0]['value'],
                'city': nearest_area['areaName'][0]['value'],
                'temperature': current_condition['temp_C'],
                'feels_like': current_condition['FeelsLikeC'],
                'humidity': current_condition['humidity'],
                'description': current_condition['lang_ru'][0]['value'],
                'wind_speed': current_condition['windspeedKmph'],
                'wind_direction': current_condition['winddir16Point'],
                'pressure': current_condition['pressure']
            }
            response = render(request, 'weather_report/index.html', {'weather_info': weather_info})
            response.set_cookie('last_city', base64.b64encode(city.encode('utf-8')).decode('utf-8'))

            if city not in search_history:
                search_history.append(city)
                if len(search_history) > 15:
                    search_history.pop(0)
                response.set_cookie('search_history', base64.b64encode(json.dumps(search_history).encode('utf-8')).decode('utf-8'))
            return response

    search_history_data = []
    for city in search_history:
        history_response = requests.get(f'https://wttr.in/{city}?format=4')
        if history_response.status_code == 200:
            search_history_data.append({
                'city': city,
                'weather': history_response.text.strip()
            })

    return render(request, 'weather_report/index.html', {'weather_info': weather_info, 'last_city': last_city, 'search_history_data': search_history_data})
