from django.urls import path
from . import views


urlpatterns = [
    path('my-cars', views.getUserCars, name='my-cars'),
    path('add', views.addCar, name='add-reservation-api'),
    # TODO: path('delete', views.deleteCar, name='delete-reservation')
]