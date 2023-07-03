from django.db import models

# Create your models here.
class Feedback(models.Model):
    date    = models.DateField(auto_now=True)
    by      = models.CharField(max_length=40)
    message = models.CharField(max_length=500)