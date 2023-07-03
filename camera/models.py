from django.db import models
from core.models import Floor

class Camera(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True)
    name  = models.CharField(max_length=100)

    TYPE_CHOICES = (
        ('Entry Camera', 'Entry Camera'),
        ('Exit Camera', 'Exit Camera'),
        ('Security', 'Security')
    )
    cam_type = models.CharField(max_length=100, null=False, choices=TYPE_CHOICES)
    path     = models.CharField(max_length=250, null=True, blank='')

