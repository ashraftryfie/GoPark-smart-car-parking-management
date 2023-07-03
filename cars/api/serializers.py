from rest_framework.serializers import ModelSerializer
from core.models import Car, Brand

class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = (
            'id',
            'brand',
            'plate_number',
            'color'
        )
        depth = 1

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            'name',
            'model'
        )