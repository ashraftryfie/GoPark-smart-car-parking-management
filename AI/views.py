from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .AI_models.Car_Color_Prediction.CarColorPrediction import getCarColor
from .AI_models.Car_Plate_Recognition.CarPlateRecognition_Test import getCarPlateNumber
from .AI_models.Car_Brand.carBrand import getCarBrand
from .AI_models.YOLOv5.detect import run
from core.models import Car, Parking, Brand, Floor
from settings.models import Setting
from multiprocessing import Process, Value
import datetime, time
import shutil


@api_view(['POST'])
@permission_classes([])
def carIsEntering(request):
    start = time.time()
    carBrand, carModel = getCarBrand(request.POST.get('imagePath'))
    carColor           = getCarColor(request.POST.get('imagePath'))

    # run YOLOv5
    run()
    carPlateNumber = getCarPlateNumber('AI/AI_models/YOLOv5/runs/detect/exp/crops/Car-Plate-Number/car.jpg')
    # shutil.rmtree('AI/AI_models/YOLOv5/runs/detect/exp')    # delete last detected results

    end = time.time()
    print('Time needed: ', (end-start))
    print(carBrand, carModel, carColor, carPlateNumber)

    if carColor != None and carPlateNumber != None and carBrand != None:
        if not isRegistered(carBrand, carModel, carColor, carPlateNumber):   
            car = registerCar(carBrand, carModel, carColor, carPlateNumber)   
        else:
            car = getCar(carBrand, carModel, carColor, carPlateNumber)

        parking, is_reserved = isReserved(car)

        if is_reserved:
            updateCarParkingWhenComes(parking)
        else:
            addCarParking(car) 

        # return True,
        return Response('Registred Successfully')          

    # return False, "Can't capture car info"
    return Response("Can't capture car info")


@api_view(['POST'])
@permission_classes([])
def carIsLeaving(request):  
    carBrand, carModel = getCarBrand(request.POST.get('imagePath'))
    carColor           = getCarColor(request.POST.get('imagePath'))
    
    # run YOLOv5
    run(source='AI/AI_models/YOLOv5/cars_outgoing')
    carPlateNumber = getCarPlateNumber('AI/AI_models/YOLOv5/runs/detect/exp/crops/Car-Plate-Number/car.jpg')
    # shutil.rmtree('AI/AI_models/YOLOv5/runs/detect/exp')    # delete last detected results

    end = time.time()

    if carColor != None and carPlateNumber != None and carBrand != None:           
        car = getCar(carBrand, carModel, carColor, carPlateNumber)

        parking, is_reserved = isReserved(car)

        if is_reserved:
            parkingCost = updateCarParkingWhenLeaves(parking)
        else:
            parkingCost = completeCarParkingInfo(car)
            # return True,
            return Response({'Parking Cost': parkingCost})
        
    # return False
    return Response("Can't capture car info")


# check if the car is registered in the DB
def isRegistered(brand, model, color, plate_number):
    if model == 'Unknown':
        car_brand = Brand.objects.get(
        name = brand
    )
    else:
        car_brand = Brand.objects.get(
            name  = brand,
            model = model
    )

    return Car.objects.filter(
        brand        = car_brand,
        color        = color,
        plate_number = plate_number
    ).exists()


# check if the car is reserved from mobile application
def isReserved(car):
    parking = Parking.objects.filter(
        car=car,
        parking_type='Reserved',
        entry_date=datetime.date.today()
    ).first()

    return parking, True if parking else False


# add car record to the DB
def registerCar(brand, model, color, plate_number):
    if model == 'Unknown':
        car_brand = Brand.objects.get(
        name = brand
    )
    else:
        car_brand = Brand.objects.get(
            name  = brand,
            model = model
    )

    car = Car.objects.create(
        brand        = car_brand,
        color        = color,
        plate_number = plate_number 
    )
    return car


# get car object
def getCar(brand, model, color, plate_number):
    if model == 'Unknown':
        car_brand = Brand.objects.get(
        name = brand
    )
    else:
        car_brand = Brand.objects.get(
            name  = brand,
            model = model
    )

    return Car.objects.get(
        brand        = car_brand,
        color        = color,
        plate_number = plate_number
    )


# add parking for the car
def addCarParking(car):
    # get first free parking
    floor = Floor.objects.filter(
        is_free=True
    ).first()

    Parking.objects.create(
        car          = car,
        floor        = floor,                
        parking_type = 'Visitor',
        entry_date   = datetime.datetime.now().date(),
        entry_time   = datetime.datetime.now().time(),
        status       = 'Active'
    )
    
    floor.busy_parks += 1   # increase number of busy parks in the floor

    if floor.busy_parks == floor.num_of_parks:  # check if the busy park equalized num of parks
        floor.is_free = False                   # then set is_free to False
        
    floor.save()


# update car parking which has reserved from the app
def updateCarParkingWhenComes(parking):  # for cars which has reservation
    # get first free parking
    floor = Floor.objects.filter(
        is_free=True
    ).first()

    parking.floor  = floor
    parking.status = 'Active'

    parking.save()

    floor.busy_parks += 1   # increase number of busy parks in the floor

    if floor.busy_parks == floor.num_of_parks:  # check if the busy park equalized num of parks
        floor.is_free = False                   # then set is_free to False
        
    floor.save()


# update the reserved car parking when it leaves
def updateCarParkingWhenLeaves(parking):
    parking.status = 'Finished'
    
    if datetime.datetime.now().time() > parking.end_time:   # if the customer has spent time more than the reserved time

        extra_hours   = datetime.datetime.now().time().hour - parking.end_time.hour
        extra_minutes = datetime.datetime.now().time().minute - parking.end_time.minute
        parked_time   = extra_hours + extra_minutes / 60
        extra_cost    = (parked_time * Setting.objects.first().hourly_cost * 1.25)
        parking.cost  += extra_cost
        parking.save()
        return extra_cost

    else:
        parking.save()
        return 0
        

# complete parking info when car leaves
#  and calculate its parking cost
def completeCarParkingInfo(car):    # for cars which has no reservation
    # get car parking
    carParking = Parking.objects.filter(car=car).first()

    end_date = datetime.datetime.now().date()
    end_time = datetime.datetime.now().time()

    # calculate parking cost
    parked_hours   = end_time.hour - carParking.entry_time.hour
    parked_minutes = end_time.minute - carParking.entry_time.minute
    parked_time = parked_hours + parked_minutes / 60
    parkingCost = parked_time * Setting.objects.first().hourly_cost

    # complete car parking info
    carParking.end_date = end_date
    carParking.end_time = end_time
    carParking.cost     = parkingCost
    
    # decrease the number of bust parks in the floor
    carParking.floor.busy_parks -=1
    carParking.floor.save()

    # set parking status to Finished
    carParking.status = 'Finished'

    carParking.save()

    # return parking cost
    return parkingCost

    