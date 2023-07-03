from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),
    path('admin-feedback', views.admin_feedback_view, name='admin-feedback'),
    path('admin-report', views.admin_report_view, name='admin-report'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout')
]

