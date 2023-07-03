from django.shortcuts import get_object_or_404, render, redirect
from core.models import Car, User, Parking
from .forms import CarForm, AdminCarAddForm
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.db.models import Q



def car_home(request):
    context = {}
    return render(request, 'admin_car_home.html', context)


def car_list(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''    # filtering value (Brand)

    car_list = Car.objects.filter(
        Q(brand__name__icontains=q)  |
        Q(brand__model__icontains=q) |
        Q(plate_number__icontains=q)  |
        Q(owner__first_name__icontains=q) |
        Q(owner__last_name__icontains=q)
    )
    
    car_list = list(reversed(car_list))

    carParkingsCount = []

    for car in car_list:
        carParkingsCount.append(Parking.objects.filter(
            car_id = car.id
        ).count())        

    # packing the two lists
    data = zip(car_list, carParkingsCount)

    return render(request, 'admin_car_list.html', {'data': data}) 


# new [edit admin_car_detail.html]
def car_detail(request, pk):
    car = Car.objects.get(id=pk)
    parkings = Parking.objects.filter(
        car_id = car.id
    ).count()

    context = {'car': car, 'parkings': parkings}
    return render(request, 'admin_car_detail.html', context)


def customerCarsPage(request, pk):
    customerCars = Car.objects.filter(
        owner_id = pk
    )
    return render(request, 'admin_car_list.html', {'data': customerCars}) #zip(customers, car_list)


def add_car(request):
    form = CarForm()
    form2 = AdminCarAddForm()

    if request.method == 'POST':
        form = CarForm(request.POST)
        form2 = AdminCarAddForm(request.POST)

        if form.is_valid() and form2.is_valid():
            myform = form.save(commit=False)
            myform.brand = form2.cleaned_data['brand']
            myform.save()
            messages.success(request, 'Car Added Successfully')
            return redirect(reverse('cars:car-list'))

        else:
            print("form is invalid")

    mydict = {'form': form, 'form2': form2}
    return render(request,'admin_car_add.html', mydict)


def car_delete(request, pk):
    requests = Car.objects.get(id=pk)
    requests.delete()
    return redirect('cars:car-list')

def car_update(request, id):
    # dictionary
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Car, id = id)
 
    # pass the object as instance in form
    form = CarForm(request.POST or None, instance = obj)
    form2 = AdminCarAddForm(request.POST or None)
    
    # save the data from and redirect to detail_view
    if form.is_valid() and form2.is_valid():
        myform = form.save(commit=False)
        myform.brand = form2.cleaned_data['brand']
        myform.save()
        messages.success(request, 'Car Updated Successfully')
        return redirect(reverse('cars:car-list'))

    else:
        print("form is invalid")
 
    # add form dictionary to context
    context = {'form':  form, 'form2': form2 }
 
    return render(request,'admin_car_add.html', context)