from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path("api/get_route/", views.get_route, name="get_route"),
]