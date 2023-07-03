from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.parkings_main, name='parkings-home'),
    path('view', views.showParkings, name='show-parkings'),
    path('car-parkings/<str:pk>', views.carParkingsPage, name='car-parking'),
    path('add', views.addParking, name='add-parking'),
    path('update/<str:pk>', views.updateParking, name='update-parking'),
    path('delete/<str:pk>', views.deleteParking, name='delete-parking'),

    path('api/', include('parkings.api.urls'))
]