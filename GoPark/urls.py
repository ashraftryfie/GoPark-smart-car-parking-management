from django.contrib import admin
from django.urls import path, include
from core import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('AI/', include('AI.urls')),
    path('camera/', include('camera.urls')),
    path('', include('core.urls')),
    path('park/', include('parkings.urls')),
    path('cars/', include('cars.urls')),
    path('users/', include('user.urls')),
    path('floors/', include('floors.urls')),
    path('settings/', include('settings.urls')),
    path('feedbacks/', include('feedbacks.urls'))
]