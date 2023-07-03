from core.models import Car, Parking
from .serializers import CarSerializer, ParkingSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import generics


@api_view(['GET'])
def cars_count_view(request, format=None):
    car_count = Car.objects.all().count()
    content = {'car_count': car_count}
    return Response(content)


@api_view(['GET'])
def floor_cars_count_view(request, id):
    floor_cars_count = Parking.objects.filter(park__floor=id, park__is_free=False).count()
    content = {'floor_cars_count': floor_cars_count}
    return Response(content)
    

@api_view(['GET'])
def calulate_car_cost(request, id):
    car_parking = Parking.objects.filter(car__id=id).first()
    car_cost = ParkingSerializer(car_parking, many=False).data['cost']
    content = {'car_cost': car_cost}
    return Response(content)