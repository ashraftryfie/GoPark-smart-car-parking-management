import email
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Setting
from .forms import SettingsForm

def site_settings(request):
    settings = Setting.objects.first()
    settingsForm = SettingsForm()

    if request.method == 'POST':   
        print(settings.reserved_hour_cost)     
        Setting.objects.update(
            garage_name        = request.POST.get('garage_name'),
            email              = request.POST.get('email'),
            phone              = request.POST.get('phone'),
            address            = request.POST.get('address'),
            hourly_cost        = request.POST.get('hourly_cost'),
            reserved_hour_cost = request.POST.get('reserved_hour_cost')
        )

        return redirect(reverse('settings:site-settings'))

    context = {'form': settingsForm, 'settings': settings}
    return render(request, 'admin_settings.html', context)