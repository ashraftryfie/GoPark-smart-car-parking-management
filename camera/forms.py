from django.forms import Form, ModelForm
from .models import Camera


class CameraForm(ModelForm):
    class Meta:
        model = Camera
        fields = '__all__'