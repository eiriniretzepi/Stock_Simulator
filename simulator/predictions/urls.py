from django.urls import path, include
from . import views

urlpatterns = [
    path('predictions', views.predictions, name="predictions"),
]
