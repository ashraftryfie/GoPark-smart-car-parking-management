from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import ParkingSerializer, ReservationSerializer
from core.models import Car, Parking
from settings.models import Setting



@api_view(['POST'])
@permission_classes([])
def addReservation(request):
    reservationSerializer = ReservationSerializer(data=request.data)

    user = request.user

    # check if user is authenticated
    if user.is_authenticated:

        # check if data is valid
        if reservationSerializer.is_valid():

            car = Car.objects.get(id=request.POST.get('car_id'))

            # calculate parking cost
            parked_hours    = reservationSerializer.validated_data['end_time'].hour - reservationSerializer.validated_data['entry_time'].hour
            parked_minutes  = reservationSerializer.validated_data['end_time'].minute - reservationSerializer.validated_data['entry_time'].minute
            parked_time     = parked_hours + parked_minutes / 60
            reservationCost = parked_time * Setting.objects.first().reserved_hour_cost
            
            # save reservation object
            Parking.objects.create(
                car              = car,
                parking_type     = 'Reserved',
                entry_date       = reservationSerializer.validated_data['entry_date'],
                entry_time       = reservationSerializer.validated_data['entry_time'],
                end_date         = reservationSerializer.validated_data['end_date'],
                end_time         = reservationSerializer.validated_data['end_time'],
                cost             = reservationCost,
                status           = 'Pending'
            )

            return Response({
                'Message'      : 'Your reservation has been set successfully !',
                'parking_cost' : reservationCost,
                'Floor'        : 4
            })

        return Response({'error': 'data is not valid'}, status=400)

    return Response({'error': 'user not authenticated'}, status=400)


@api_view(['GET'])
@permission_classes([])
def getUserReservations(request):

    # get user from request
    user = request.user

    userCar = Car.objects.filter(
        owner=user
    ).first()

    # get all user's reservations
    userReservations = Parking.objects.filter(
        car = userCar,
        parking_type='Reserved'
    )

    if userReservations.count() == 0:
        return Response({
            'message': 'No reservations yet'
        })
        
    serializer = ParkingSerializer(userReservations, many=True)

    return Response(serializer.data)


# TODO update Reservation view
# @api_view(['POST'])
# def updateReservation(request):
#


@api_view(['POST'])
@permission_classes([])
def deleteReservation(request):
    reservationID = request.POST.get('id')

    if reservationID != None:
        reservation = Parking.objects.get(id=reservationID)
        if reservation != None:
            reservation.delete()
            return Response({
                'message': 'Deleted Successfully !'
            })

    return Response({   # otherwise
        'error': 'Error !'
    })


    