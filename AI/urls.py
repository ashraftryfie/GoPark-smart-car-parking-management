from django.urls import path
from . import views

urlpatterns = [
    path('carIsEntering', views.carIsEntering),
    path('carIsLeaving', views.carIsLeaving)
]