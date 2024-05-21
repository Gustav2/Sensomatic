from django.urls import path

from . import views

urlpatterns = [
    path('handle_post/', views.handle_post, name='handle_post'),
    path('sorting_algorithm/', views.sorting_algorithm, name='sorting_algorithm'),
    path('import_addresses/', views.import_addresses, name='import_addresses'),
    path('api_sort/', views.api_sort, name='api_sort'),
    path('all_route/', views.all_route, name='all_route'),
    path('route_from_percentage/<int:percentage>/', views.route_from_percentage, name='route_from_percentage'),
]