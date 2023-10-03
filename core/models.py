from django.db import models

class WeekDistance(models.Model):
    distance = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
