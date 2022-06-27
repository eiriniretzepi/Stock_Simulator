from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('stocks/', include('stocks.urls')),
    path('predictions/', include('predictions.urls')),
]
