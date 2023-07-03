from django.urls import path, include
from user import views




    ############################# users ##########################################


urlpatterns = [


    path('manage-users', views.manage_users, name='manage-users'),
    path('users-view', views.users_view, name='users-view'),
    path('add-user', views.add_user, name='add-user'),
    path('delete-user/<int:pk>', views.delete_user, name='delete-user'),
    path('update-user/<int:pk>', views.update_user, name='update-user'),


    # users api's for registration, login and logout
    path('api/', include('user.api.urls')),


    ############################ customer ##########################################
    path('admin-view-customer-invoice', views.admin_view_customer_invoice_view, name='admin-view-customer-invoice'),
    path('Show-details-invoice/<int:pk>', views.update_user, name='Show-details-invoice'),
    path('admin-view-customer-enquiry', views.admin_view_customer_enquiry_view, name='admin-view-customer-enquiry'),






]