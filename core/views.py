from django.shortcuts import render, redirect
from . import models
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.db.models import Q
from django.http import HttpResponseRedirect
from core import models
from feedbacks.models import Feedback
from django.contrib.auth.hashers import make_password



# ============================================================================================
# ADMIN RELATED views start
# ============================================================================================


def home_view(request):
    if request.user.is_authenticated == False :
        return HttpResponseRedirect('login')

    return HttpResponseRedirect('admin-dashboard')


def afterlogin_view(request):
    return redirect('admin-dashboard')


# @login_required(login_url='adminlogin')
def admin_dashboard_view(request):

    dict = {
        'total_customers': models.User.objects.all().count(),
        'total_cars': models.Car.objects.all().count(),
        'total_parkings': models.Parking.objects.all().count(),
        'available_parks': 10, 
        'total_feedback': 5,
        'total_parks': 10, 
        'total_car_parkings': 10,
        'data': zip([10], [10]),
    }

    return render(request, 'vehicle/admin_dashboard.html', context=dict)


def admin_report_view(request):
    dict = {}
    return render(request, 'vehicle/admin_report.html', context=dict)


def admin_feedback_view(request):
    return render(request, 'vehicle/admin_feedback.html', {})


def loginUser(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)
            return HttpResponseRedirect('admin-dashboard')

        else:
            return render(request, 'vehicle/adminlogin.html')


    return render(request, 'vehicle/adminlogin.html')


def logoutUser(request):
    logout(request)
    return render(request, 'vehicle/adminlogin.html')
