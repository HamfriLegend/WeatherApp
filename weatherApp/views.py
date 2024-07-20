import json
from urllib.parse import quote, unquote
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from weatherApp.WeatherAPI import WeatherAPI
from .models import CitySearchCount


# Create your views here.
class WeatherView(View):
    def get(self, request):
        lat = request.GET.get('lat', None)
        lng = request.GET.get('lon', None)
        if lat is not None and lng is not None:
            lat = float(lat)
            lng = float(lng)
            city = request.GET.get('city', None)
            weather_api = WeatherAPI(lat, lng)
            forecast_week = weather_api.get_forecasts()
            forecasts_24 = weather_api.get_day_forecast()
            cities_cookie = request.COOKIES.get('city_search', '[]')
            lats_cookie = request.COOKIES.get('lat_search', '[]')
            lons_cookie = request.COOKIES.get('lon_search', '[]')

            city_record: CitySearchCount = CitySearchCount.objects.filter(city=city, lat=lat, lon=lng).first()
            if city_record:
                city_record_new = CitySearchCount(city=city, lat=lat, lon=lng,search_count=city_record.search_count+1)
                city_record_new.save()
            else:
                city_record_new = CitySearchCount(city=city, lat=lat, lon=lng,search_count=1)
                city_record_new.save()

            try:
                cities = json.loads(unquote(cities_cookie)) if cities_cookie else []
                lats = json.loads(unquote(lats_cookie)) if lats_cookie else []
                lons = json.loads(unquote(lons_cookie)) if lons_cookie else []
            except json.JSONDecodeError:
                cities = []
                lats = []
                lons = []

            if city and lat and lng and lat not in lats and lng not in lons:
                cities.append(city)
                lats.append(lat)
                lons.append(lng)

            response = render(request, 'index.html', context = {"forecasts_week":forecast_week,
                                                                            "city":city,
                                                                            "forecasts_24":forecasts_24,
                                                                            "times":range(24)})
            print(forecasts_24)
            response.set_cookie('city_search', quote(json.dumps(cities)))
            response.set_cookie('lat_search', quote(json.dumps(lats)))
            response.set_cookie('lon_search', quote(json.dumps(lons)))
            return response
        else:
            return render(request, 'index.html')


class WeatherAPIView(APIView):
    def get(self, request):
        records = CitySearchCount.objects.all()
        record_dict = {}
        for record in records:
            record_dict[record.city] = {"lat": record.lat, "lon": record.lon, "search_count": record.search_count}

        return JsonResponse(record_dict, json_dumps_params={'ensure_ascii': False})
