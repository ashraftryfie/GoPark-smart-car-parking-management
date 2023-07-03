from django.forms import Form, ModelForm, ModelChoiceField
from core.models import Parking, Car, Floor


class ParkingChoiceField(Form):
        car = ModelChoiceField(
            queryset=Car.objects.all(),
            to_field_name='id'
        )

        floor = ModelChoiceField(
            queryset=Floor.objects.filter(
                is_free=True
            ), 
            to_field_name='id'
        )


class ParkingForm(ModelForm):
    class Meta:
        model  = Parking
        fields = (
            'car',
            'floor',
            'parking_type',
            'entry_date',
            'entry_time',
            'end_date',
            'end_time',
            'status',
            'cost'
        )

