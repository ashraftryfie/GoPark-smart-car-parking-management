from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from core.models import Car, Parking, Floor
from .forms import ParkingForm, ParkingChoiceField
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from settings.models import Setting


@login_required
def parkings_main(request):
    context = {}
    return render(request, 'parkings_home.html', context)


@login_required
def showParkings(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    # filtering value
    parkings = []

    if q is not '': 
        splited_phrase = q.split()
        if splited_phrase[0] == 'floor':
            parkings = Parking.objects.filter(
                Q(floor__floor_number=splited_phrase[1])
            )
            
        else:
            parkings = Parking.objects.filter(
                Q(entry_date__contains=q) |
                Q(end_date__contains=q) |
                Q(car__brand__name__contains=q) |
                Q(parking_type__contains=q) |
                Q(status__contains=q)
            )
    
    else:
        parkings = Parking.objects.all()

    context = {'parkings': parkings}
    return render(request, 'parkings_list.html', context)


@login_required
def carParkingsPage(request, pk):
    carParkings = Parking.objects.filter(
        car_id = pk
    )

    context = {'parkings': carParkings}
    return render(request, 'parkings_list.html', context)


@login_required
def addParking(request):
    parkingForm        = ParkingForm()
    parkingChoiceField = ParkingChoiceField()

    if request.method == 'POST':
        form1 = ParkingForm(request.POST)
        form2 = ParkingChoiceField(request.POST)

        if form1.is_valid() and form2.is_valid():
            form1.car   = form2.cleaned_data['car']
            form1.floor = form2.cleaned_data['floor'] 
            parking = form1.save(commit=False)

            parking.save()

            floor = parking.floor
            floor.busy_parks += 1
            if floor.busy_parks == floor.num_of_parks:
                floor.is_free = False
            floor.save()

            return redirect('show-parkings')

    context = {'form1': parkingForm, 'form2': parkingChoiceField}
    return render(request, 'parkings_add.html', context)


@login_required
def updateParking(request, pk): 
    parking = Parking.objects.get(id=pk)
    if request.method != 'POST':
        if parking.status == 'Active':
            floor = parking.floor
            floor.busy_parks -= 1
            floor.save()

    form1 = ParkingForm(instance=parking) 
    form2 = ParkingChoiceField()
    
    if request.method == 'POST':
        form1 = ParkingForm(request.POST, instance=parking)
        form2 = ParkingChoiceField(request.POST)

        if form1.is_valid() and form2.is_valid():
            form1.car   = form2.cleaned_data['car']
            form1.floor = form2.cleaned_data['floor']
            parking = form1.save(commit=False)

            parking.save()

            floor = parking.floor
            floor.busy_parks += 1
            if floor.busy_parks == floor.num_of_parks:
                floor.is_free = False
            floor.save()
            
            return redirect('show-parkings')

    context = {'form1': form1, 'form2': form2}
    return render(request, 'parkings_add.html', context)


@login_required
def deleteParking(request, pk):
    parking = Parking.objects.get(id=pk)

    if parking.status == 'Active':
        floor = parking.floor
        if floor is not None:   
            floor.busy_parks -= 1
            floor.save()    

    parking.delete()
    return redirect('show-parkings')