from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index_login_page, name = 'index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
]