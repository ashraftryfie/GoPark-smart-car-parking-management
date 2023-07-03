from django.urls import path
from . import views

urlpatterns = [
    path('home', views.homePage, name='floors-home'),
    path('view-floors', views.viewFloors, name='view-floors'),
    path('add', views.addFloor, name='add-floor'),
    path('update-floor/<str:pk>', views.updateFloor, name='update-floor'),
    path('delete-floor/<str:pk>', views.deleteFloor, name='delete-floor')
]