from django.test import TestCase, Client
from django.urls import reverse
import base64
import json
from unittest.mock import patch

class WeatherViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')

    @patch('weather_report.views.requests.get')
    def test_weather_info_display(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [{
                "temp_C": "23",
                "FeelsLikeC": "25",
                "humidity": "61",
                "lang_ru": [{"value": "Переменная облачность"}],
                "windspeedKmph": "15",
                "winddir16Point": "WNW",
                "pressure": "1011"
            }],
            "nearest_area": [{
                "areaName": [{"value": "Москва"}],
                "country": [{"value": "Russia"}]
            }]
        }
        mock_get.return_value.text = "⛅️"

        response = self.client.get(self.url, {'city': 'Москва'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Москва")
        self.assertContains(response, "Russia")
        self.assertContains(response, "23")
        self.assertContains(response, "25")
        self.assertContains(response, "61")
        self.assertContains(response, "Переменная облачность")
        self.assertContains(response, "15")
        self.assertContains(response, "WNW")
        self.assertContains(response, "1011")
        self.assertContains(response, "⛅️")

    def test_last_city_cookie(self):
        city = "Москва"
        encoded_city = base64.b64encode(city.encode('utf-8')).decode('utf-8')
        self.client.cookies['last_city'] = encoded_city

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ранее вы смотрели Москва")

    @patch('weather_report.views.requests.get')
    def test_search_history(self, mock_get):
        # Mock the API response for history
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Москва: ⛅️  🌡️+23°C 🌬️↘15km/h"

        search_history = ["Москва", "Санкт-Петербург"]
        encoded_history = base64.b64encode(json.dumps(search_history).encode('utf-8')).decode('utf-8')
        self.client.cookies['search_history'] = encoded_history

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Москва: ⛅️  🌡️+23°C 🌬️↘15km/h")
        self.assertContains(response, "Санкт-Петербург")

    @patch('weather_report.views.requests.get')
    def test_add_to_search_history(self, mock_get):
        # Mock the API response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "current_condition": [{
                "temp_C": "23",
                "FeelsLikeC": "25",
                "humidity": "61",
                "lang_ru": [{"value": "Переменная облачность"}],
                "windspeedKmph": "15",
                "winddir16Point": "WNW",
                "pressure": "1011"
            }],
            "nearest_area": [{
                "areaName": [{"value": "Москва"}],
                "country": [{"value": "Russia"}]
            }]
        }
        mock_get.return_value.text = "⛅️"

        response = self.client.get(self.url, {'city': 'Москва'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('search_history', response.cookies)
        search_history = json.loads(base64.b64decode(response.cookies['search_history'].value).decode('utf-8'))
        self.assertIn('Москва', search_history)