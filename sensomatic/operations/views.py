import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from datacollector.models import Trashcan
from operations.models import Route


# Create your views here.

def get_route(request, username=None):
    if not request.method == "GET":
        return JsonResponse({"detail": "Only GET requests are allowed."}, status=405)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"detail": "User not found"}, status=500)

    try:
        route = Route.objects.filter(user=user, completed=False).order_by("operating_date").first()
    except Route.DoesNotExist:
        route = None

    if not route:
        return JsonResponse({"detail": "No route found for given user"}, status=500)

    return JsonResponse({
        "route": route.adresses,
        "operating_date": route.operating_date,
        "completed": route.completed
    })

