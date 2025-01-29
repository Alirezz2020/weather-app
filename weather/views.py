from django.shortcuts import render
from django.views.generic import TemplateView
import requests


class WeatherView(TemplateView):
    template_name = "weather.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.request.GET.get('city', 'New York')  # Default city

        api_key = "741ecc4bfd64b39a3632783eb39f48e4"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            context['weather'] = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'pressure': data['main']['pressure'],
            }
        else:
            context['error'] = "Could not retrieve weather data."

        return context
