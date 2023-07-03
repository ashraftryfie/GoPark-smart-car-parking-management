from django.urls import path
from . import views

app_name='feedbacks'

urlpatterns = [

    path('', views.admin_feedback_view, name='admin-feedback'),
    
]