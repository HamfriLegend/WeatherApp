from django.db import models


# Create your models here.
class CitySearchCount(models.Model):
    city = models.CharField(max_length=50)
    lat = models.FloatField()
    lon = models.FloatField()
    search_count = models.IntegerField(default=0)

