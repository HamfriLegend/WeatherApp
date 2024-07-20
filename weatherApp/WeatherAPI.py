import requests
import datetime


class Forecast:
    """
    Описывает предсказание погоды на конкретную дату
    """
    def __init__(self, date:str, temp_max: float, temp_min: float, rain: float, wind_speed: float, wind_dir: float, weather_code: int):
        """

        :param date: дата в виде строки
        :param temp_max: максимальная температура
        :param temp_min: минимальная температура
        :param rain: вероятность дождя
        :param wind_speed: скорость ветра
        :param wind_dir: направление ветра
        :param weather_code: код погоды
        """
        weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        weekdays_short = ['Пн','Вт','Ср','Чт','Пт','Сб','Вс']
        weekdays_id = datetime.datetime.strptime(date.split('T')[0], '%Y-%m-%d').weekday()
        self.day = weekdays[weekdays_id]
        self.day_short = weekdays_short[weekdays_id]
        self.date = date.split('T')[0].split('-')[2]+'.'+date.split('T')[0].split('-')[1]
        self.temp_max = temp_max
        self.temp_min = temp_min
        self.rain = rain
        self.wind_speed = wind_speed
        if 0 <= wind_dir < 45:
            self.wind_dir = "С"
        elif wind_dir >= 45 and wind_dir > 90:
            self.wind_dir = "С-В"
        elif 90 <= wind_dir < 135:
            self.wind_dir = "В"
        elif 135 <= wind_dir < 180:
            self.wind_dir = "Ю-В"
        elif 180 <= wind_dir < 225:
            self.wind_dir = "Ю"
        elif 225 <= wind_dir < 270:
            self.wind_dir = "Ю-З"
        elif 270 <= wind_dir < 315:
            self.wind_dir = "З"
        elif 315 <= wind_dir < 360:
            self.wind_dir = "С-З"
        else: self.wind_dir = "С"

        weather_codes = {
            0:"sun",
            1:"cloud-sun",
            2:"cloud",
            3:"2cloud",
            45:"cloud-fog",
            48:"fog",
            51:"rain-sun",
            53:"rain-sun",
            55:"rain",
            56:"rain-sun",
            57:"rain",
            61:"rain",
            63:"rain",
            65:"f-rain",
            66:"f-rain",
            67:"f-rain",
            71:"snow",
            73:"snow",
            75:"f-snow",
            77:"snow",
            80:"f-rain",
            81:"f-rain",
            82:"f-rain",
            85:"snow",
            86:"f-snow",
            95:"thunderstorm",
            96:"thunderstorm",
            99:"thunderstorm-rain",
        }

        self.weather = weather_codes[weather_code]


class Forecast24:
    """
    Описывает предсказание погоды на 24 часа
    """
    def __init__(self, temps: [float], wind_speeds: [float], wind_dirs: [float], weather_codes: [int]):
        self.dates = []
        for i in (range(24)):
            self.dates.append(f"{i}:00")
        self.temps = temps
        self.wind_speeds = wind_speeds
        self.wind_dirs = []
        for wind_dir in wind_dirs:
            if 0 <= wind_dir < 45:
                self.wind_dirs.append("С")
            elif wind_dir >= 45 and wind_dir > 90:
                self.wind_dirs.append("С-В")
            elif 90 <= wind_dir < 135:
                self.wind_dirs.append("В")
            elif 135 <= wind_dir < 180:
                self.wind_dirs.append("Ю-В")
            elif 180 <= wind_dir < 225:
                self.wind_dirs.append("Ю")
            elif 225 <= wind_dir < 270:
                self.wind_dirs.append("Ю-З")
            elif 270 <= wind_dir < 315:
                self.wind_dirs.append("З")
            elif 315 <= wind_dir < 360:
                self.wind_dirs.append("С-З")
            else:
                self.wind_dirs.append("С")

        weather_codes_dict = {
            0:"sun",
            1:"cloud-sun",
            2:"cloud",
            3:"2cloud",
            45:"cloud-fog",
            48:"fog",
            51:"rain-sun",
            53:"rain-sun",
            55:"rain",
            56:"rain-sun",
            57:"rain",
            61:"rain",
            63:"rain",
            65:"f-rain",
            66:"f-rain",
            67:"f-rain",
            71:"snow",
            73:"snow",
            75:"f-snow",
            77:"snow",
            80:"f-rain",
            81:"f-rain",
            82:"f-rain",
            85:"snow",
            86:"f-snow",
            95:"thunderstorm",
            96:"thunderstorm",
            99:"thunderstorm-rain",
        }

        self.weather_codes = list(map(lambda x: weather_codes_dict[x], weather_codes))


class WeatherAPI:
    """
    Класс, предоставляющий методы для порлучаения данных с API https://open-meteo.com
    """
    def __init__(self, lat: float, lng: float):
        self.__API_URL = "https://api.open-meteo.com/v1/forecast"
        self.__header = {"User-Agent": "WeatherApp", "Accept": "application/json"}
        response = requests.get(f"{self.__API_URL}?latitude={lat}&longitude={lng}&hourly=temperature_2m"
                                f",precipitation_probability,"
                                f"weather_code,wind_speed_10m,wind_direction_10m", self.__header)
        self.__json_response = response.json()['hourly']
        self.times = self.__json_response['time']
        count = len(self.times)
        temps = self.__json_response['temperature_2m']
        self.temps_24 = [temps[i:i + 24] for i in range(0, count, 24)]

        precipitation_probability = self.__json_response['precipitation_probability']
        self.precipitation_probability_24 = [precipitation_probability[i:i + 24] for i in range(0, count, 24)]

        weather_code = self.__json_response['weather_code']
        self.weather_code_24 = [weather_code[i:i + 24] for i in range(0, count, 24)]

        wind_speed_10m = self.__json_response['wind_speed_10m']
        self.wind_speed_10m_24 = [wind_speed_10m[i:i + 24] for i in range(0, count, 24)]

        wind_direction_10m = self.__json_response['wind_direction_10m']
        self.wind_direction_10m_24 = [wind_direction_10m[i:i + 24] for i in range(0, count, 24)]

    def get_forecasts(self) -> list[Forecast]:
        """
        Выдает погоду на неделю вперед
        :return: список Forecast, в котором содержится инфомация о погоде (1 день это текущий)
        """
        dates = set()
        times = self.__json_response['time']
        for date in times:
            unic_date = date.split('T')[0]
            dates.add(unic_date)
        dates = sorted(dates)
        count = len(times)


        result = []
        hour = datetime.datetime.now().hour
        for i in range(7):
            date = dates[i]
            temp_min = min(self.temps_24[i])

            if i==0:
                temp_max = self.temps_24[i][hour]
                rain = self.precipitation_probability_24[i][hour]
                wind_speed = self.wind_speed_10m_24[i][hour]
                wind_dir = self.wind_direction_10m_24[i][hour]
                weather_code = self.weather_code_24[i][hour]
            else:
                temp_max = max(self.temps_24[i])
                rain = max(self.precipitation_probability_24[i])
                wind_speed = max(set(self.wind_speed_10m_24[i]), key = self.wind_speed_10m_24[i].count)
                wind_dir = max(set(self.wind_direction_10m_24[i]), key = self.wind_direction_10m_24[i].count)
                weather_code = max(set(self.weather_code_24[i]), key = self.weather_code_24[i].count)

            forecast = Forecast(date, temp_min, temp_max, rain, wind_speed, wind_dir, weather_code)
            result.append(forecast)

        return result

    def get_day_forecast(self):
        """
        Возвращает почасовое предсказание погоды на 7 дней (1 день текущий)
        :return:
        """
        forecasts = []
        for i in range(7):
            forecasts.append(Forecast24(
                self.temps_24[i],
                self.wind_speed_10m_24[i],
                self.wind_direction_10m_24[i],
                self.weather_code_24[i]
            ))

        return forecasts



