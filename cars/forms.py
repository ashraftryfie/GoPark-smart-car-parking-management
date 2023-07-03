from django import forms
from django.contrib.auth.models import User
from core.models import Car, Parking, Brand, User


class AdminCarAddForm(forms.Form):
    owner = forms.ModelChoiceField(
        queryset=User.objects.all(), to_field_name='id'
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(), to_field_name='id'
    )

class CarForm(forms.ModelForm):
    class Meta:
        model   = Car
        fields  = '__all__'
        widgets = { }