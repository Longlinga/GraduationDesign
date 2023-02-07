from django.db import models


# Create your models here.
class jd_data(models.Model):
    d_titel = models.CharField(max_length=255)
    d_price = models.FloatField()
    add_time = models.DateTimeField()

class user_subscription(models.Model):
    user_id = models.BigIntegerField()
    commodity_id = models.CharField(max_length=255)