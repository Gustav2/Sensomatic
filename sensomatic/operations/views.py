from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from operations.models import Route


# Create your views here.

def get_route(request):
    if request.method == "GET":
        user = User.objects.get(username="admin")
        route = Route.objects.filter(user=user, completed=False).order_by("operating_date").first()

        if route:
            return JsonResponse({
                "route": route.adresses,
                "operating_date": route.operating_date,
                "completed": route.completed
            })



    return None