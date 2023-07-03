from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CarSerializer, BrandSerializer
from core.models import Car, Brand



@api_view(['POST'])
@permission_classes([])
def addCar(request):
    carSerializer   = CarSerializer(data=request.data)
    brandSerializer = BrandSerializer(data=request.data)

    user = request.user

    if user.is_authenticated:
        if carSerializer.is_valid() and brandSerializer.is_valid():

            brand, _ = Brand.objects.get_or_create(
                name  = brandSerializer.validated_data['name'],
                model = brandSerializer.validated_data['model']
            )

            Car.objects.create(
                owner = user,
                brand = brand,
                plate_number = carSerializer.validated_data['plate_number'],
                color        = carSerializer.validated_data['color']
            )
            return Response('Car Added Successfully!')
        else:
            return Response('Info Is Not Valid')
    else:
        return Response('Please Login First')


@api_view(['GET'])
@permission_classes([])
def getUserCars(request):
    user = request.user

    userCars = Car.objects.filter(
        owner = user
    )

    if userCars.count() == 0:
        return Response({
            'message': 'You have No Cars'
        })

    serializer = CarSerializer(userCars, many=True)
    return Response(serializer.data)