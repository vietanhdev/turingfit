from django.db import models

class WeekDistance(models.Model):
    week = models.DateField(null=True)
    distance = models.FloatField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    unique_together = ('week', 'user')
