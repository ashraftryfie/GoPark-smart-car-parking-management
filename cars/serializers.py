from rest_framework.serializers import ModelSerializer
from core.models import Car, Parking


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'

