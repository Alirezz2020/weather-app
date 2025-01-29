# from django.shortcuts import render
# from django.views.generic import TemplateView
# import requests
#
#
# class WeatherView(TemplateView):
#     template_name = "weather.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         city = self.request.GET.get('city', 'New York')  # Default city
#
#         api_key = "741ecc4bfd64b39a3632783eb39f48e4"
#         url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
#
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             context['weather'] = {
#                 'city': data['name'],
#                 'temperature': data['main']['temp'],
#                 'description': data['weather'][0]['description'],
#                 'icon': data['weather'][0]['icon'],
#                 'humidity': data['main']['humidity'],
#                 'wind_speed': data['wind']['speed'],
#                 'pressure': data['main']['pressure'],
#             }
#         else:
#             context['error'] = "Could not retrieve weather data."
#
#         return context
from django.shortcuts import render
from django.views.generic import TemplateView
import requests


class WeatherView(TemplateView):
    template_name = "weather.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        city = self.request.GET.get('city', 'New York')  # Default to New York if no city is specified
        api_key = "741ecc4bfd64b39a3632783eb39f48e4"

        # Current weather data URL
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        # Forecast data URL (5-day forecast)
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&cnt=5"

        # Requesting current weather data
        weather_response = requests.get(weather_url)
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            context['weather'] = {
                'city': weather_data['name'],
                'temperature': weather_data['main']['temp'],
                'description': weather_data['weather'][0]['description'],
                'icon': weather_data['weather'][0]['icon'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed'],
                'pressure': weather_data['main']['pressure'],
            }
        else:
            context['error'] = "Could not retrieve weather data."

        # Requesting forecast data
        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            context['forecast'] = []
            for item in forecast_data['list']:
                context['forecast'].append({
                    'date': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                })
        else:
            context['forecast_error'] = "Could not retrieve forecast data."

        return context
