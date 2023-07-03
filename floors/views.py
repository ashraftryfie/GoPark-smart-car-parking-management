from django.shortcuts import render, redirect, HttpResponse
from core.models import Floor
from .forms import FloorForm
import requests


def homePage(request):
    return render(request, 'floors_home.html')


def viewFloors(request):
    floors = Floor.objects.all()
    context = {'floors': floors}
    return render(request, 'floors_list.html', context)


def addFloor(request):
    floorForm = FloorForm()

    if request.method == 'POST':
        floorForm = FloorForm(request.POST)
        if floorForm.is_valid():
            floorForm.save()
            return redirect('view-floors')

    context = {'form': floorForm}
    return render(request, 'floor_add.html', context)


def updateFloor(request, pk):
    floor     = Floor.objects.get(id=pk)
    floorForm = FloorForm(instance=floor)

    if request.method == 'POST':
        floorForm = FloorForm(request.POST, instance=floor)
        if floorForm.is_valid():
            floorForm.save()
            return redirect('view-floors')    

    context = {'form': floorForm}
    return render(request, 'floor_add.html', context)


def deleteFloor(request, pk):
    Floor.objects.get(id=pk).delete()  
    return redirect('view-floors')