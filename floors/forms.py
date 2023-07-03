from django.forms import Form, ModelForm
from core.models import Floor


class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = (
            'floor_number',
            'num_of_parks'
        )