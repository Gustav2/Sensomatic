from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('api/get_route/<str:username>', views.get_route, name="get_route"),
    path('api/generate_route', views.generate_route, name="generate_route"),
]