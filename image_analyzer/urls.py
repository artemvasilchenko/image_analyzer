"""image_analyzer URL Configuration"""
from django.urls import path, include

urlpatterns = [
    path('', include('app_image_analyzer.urls'))
]
