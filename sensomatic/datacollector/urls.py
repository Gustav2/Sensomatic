from django.urls import path

from . import views

urlpatterns = [
    path('handle_post/', views.handle_post, name='handle_post'),
    path('sorting_algorithm/', views.sorting_algorithm, name='sorting_algorithm'),
    path('import_addresses/', views.import_addresses, name='import_addresses'),
]