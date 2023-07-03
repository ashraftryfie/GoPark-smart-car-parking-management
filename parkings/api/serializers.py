from rest_framework.serializers import ModelSerializer
from core.models import Parking

class ReservationSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = (
            'car_id',
            'entry_date',
            'entry_time',
            'end_date',
            'end_time'
        )

class ParkingSerializer(ModelSerializer):
    class Meta:
        model = Parking
        fields = (
            'id',
            'entry_date',
            'entry_time',
            'end_date',
            'end_time',
            'cost',
            'status'
        )