from django.db import models

# Create your models here.
class Setting(models.Model):
    garage_name        = models.CharField(max_length=100)
    email              = models.EmailField(unique=True, null=True)
    phone              = models.IntegerField(null=True, blank=True)
    address            = models.CharField(max_length=100)
    hourly_cost        = models.IntegerField()
    reserved_hour_cost = models.IntegerField()