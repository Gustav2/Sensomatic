from django.urls import path

from . import views

urlpatterns = [
    path('handle_post/', views.handle_post, name='handdle_post')
]
