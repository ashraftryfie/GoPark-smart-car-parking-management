from django.urls import path
from . import views

urlpatterns = [
    path('run-cameras', views.run_cameras, name='run-cameras'),
    path('car-enters', views.entryCamera),
    path('car-exits', views.exitCamera),
    path('home', views.homePage, name='cameras-home'),
    path('view-cameras', views.viewCameras, name='view-cameras'),
    path('add', views.addCamera, name='add-camera'),
    path('update-camera/<str:pk>', views.updateCamera, name='update-camera'),
    path('delete-camera/<str:pk>', views.deleteCamera, name='delete-camera')
]