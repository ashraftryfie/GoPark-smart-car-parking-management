from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from . import models
from django.contrib.auth.models import Group
from django.db.models import Sum
from django.db.models import Q
from django.http import HttpResponseRedirect

from core import models
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from .forms import UserForm


def manage_users(request):
    return render(request, 'admin_customer.html')


def users_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 

    customers = models.User.objects.filter(
        Q(first_name__icontains=q) |
        Q(last_name__icontains=q)  |
        Q(email__icontains=q)
    )

    customerCarsCount = []

    for customer in customers:
        customerCarsCount.append(models.Car.objects.filter(
            owner_id = customer.id
        ).count())

    # TODO : calculate customer total payments


    # packing the two lists
    customerInfo = zip(customers, customerCarsCount)

    return render(request, 'admin_view_customer.html', {'customerInfo': customerInfo})


def add_user(request):
    userForm = UserForm()

    if request.method == 'POST':
            userForm = UserForm(request.POST)
            if userForm.is_valid():
                user = userForm.save(commit=False)
                user.password = make_password(user.password)
                user.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('manage-users') 
            else:
                messages.success(request, 'Info is not valid!')
                return redirect('manage-users') 

    context = {'form': userForm}
    return render(request, 'admin_add_customer.html', context)


def delete_user(request, pk):
    user = models.User.objects.get(id=pk)
    user.delete()
    return redirect('users-view')    



def update_user(request, pk):
    user = models.User.objects.get(id=pk)
    userForm = UserForm(instance=user)

    if request.method == 'POST':
            userForm = UserForm(request.POST, instance=user)
            if userForm.is_valid():
                user = userForm.save(commit=False)
                user.password = make_password(user.password)
                user.save()
                messages.success(request, 'Member was created successfully!')
                return redirect('manage-users')  
            else:
                messages.success(request, 'User Info is not valid!')
                return redirect('manage-users')  

    context = {'form': userForm}
    return render(request, 'admin_add_customer.html',context)    


def admin_view_customer_invoice_view(request):
    return render(request, 'admin_view_customer_invoice.html', {})


def admin_view_customer_enquiry_view(request):
    return render(request, 'admin_view_customer_enquiry.html', {})