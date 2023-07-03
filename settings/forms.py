from django.forms import Form, ModelForm, ModelChoiceField
from .models import Setting


class SettingsForm(ModelForm):
    class Meta:
        model  = Setting
        fields = '__all__'