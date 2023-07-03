from django.urls import path
from knox import views as knox_views
from . import views


urlpatterns = [
    path('register', views.registerUser),
    path('myinfo', views.getUser),
    path('login', views.login),
    path('logout', knox_views.LogoutView.as_view()),
]