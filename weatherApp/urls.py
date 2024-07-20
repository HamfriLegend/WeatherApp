from django.urls import path, include
from weatherApp.views import WeatherView, WeatherAPIView
urlpatterns = [
    path('', WeatherView.as_view(), name='index'),
    path('?', WeatherView.as_view(), name='index'),
    path('api/get_city_search', WeatherAPIView.as_view(), name='get_city_search'),
]