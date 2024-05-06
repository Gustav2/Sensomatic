from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index_login_page, name = 'index'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('logout/', views.logout_user, name = 'logout'),
    path('api/driverassignment/', views.add_driver, name = 'add_driver'),
    path('dashboard/indstillinger/', views.setting, name = 'settings'),
    path('dashboard/historik/', views.historik, name = 'historik'),
    path('dashboard/skraldespand/', views.skaldeniveau, name = 'skaldeniveau'),
    path('api/timeintervalassignment/', views.set_timeinterval, name='set_timeinterval'),
    path('api/addIsland', views.add_island, name="add_island"),
]