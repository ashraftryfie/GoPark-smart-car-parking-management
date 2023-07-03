from django.urls import path
from . import views

app_name='settings'

urlpatterns = [

    # Site Settings Home
    path('', views.site_settings, name='site-settings'),

    # Change Site Settings
    # path('update-settings', views.site_settings_update, name='update-settings'),

]