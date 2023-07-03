from django.shortcuts import render, redirect, HttpResponse
from .models import Camera
from .forms import CameraForm
from threading import Thread
import requests


def homePage(request):
    return render(request, 'camera_home.html')


def viewCameras(request):
    cameras = Camera.objects.all()
    context = {'cameras': cameras}
    return render(request, 'camera_list.html', context)


def addCamera(request):
    camForm = CameraForm()

    if request.method == 'POST':
        camForm = CameraForm(request.POST)
        if camForm.is_valid():
            camForm.save()
            return redirect('view-cameras')

    context = {'form': camForm}
    return render(request, 'camera_add.html', context)


def updateCamera(request, pk):
    camera  = Camera.objects.get(id=pk)
    camForm = CameraForm(instance=camera)

    if request.method == 'POST':
        camForm = CameraForm(request.POST, instance=camera)
        if camForm.is_valid():
            camForm.save()
            return redirect('view-cameras')    

    context = {'form': camForm}
    return render(request, 'camera_add.html', context)


def deleteCamera(request, pk):
    Camera.objects.get(id=pk).delete()  
    return redirect('view-cameras')





###########################################


def run_camera_1_():
    from .Car_Detection_Cam_1.takepicture import test
def run_camera_2_():
    from .Car_Detection_Cam_2.takepicture import test

def run_cameras(request):
    Thread(target=run_camera_1_).start()
    Thread(target=run_camera_2_).start()
    return HttpResponse()

def entryCamera(request):
    # payload = {'imagePath': 'C:/Users/yamen/Desktop/me.jpg'}
    # result = requests.post('http://127.0.0.1:8000/AI/carIsEntering', data=payload)
    from .Car_Detection_Cam_1.takepicture import test
    return HttpResponse()

def exitCamera(request):
    # payload = {'imagePath': 'C:/Users/yamen/Desktop/me.jpg'}
    # result = requests.post('http://127.0.0.1:8000/AI/carIsLeaving', data=payload)
    from .Car_Detection_Cam_2.takepicture import test
    return HttpResponse()