import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import SensorData, TrashIsland, Trashcan


# Create your views here.

# til test af esp
@csrf_exempt
def handle_post(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        print("Received data:", payload)

        payload["temperature"]
        payload["humidity"]

        trashisland = TrashIsland.objects.get(street_name="Test Street")
        trashcan = Trashcan.objects.get(island=trashisland)

        SensorData.objects.create(trashcan=Trashcan.objects.get(id=1), status = 0, temperature=payload["temperature"], humidity=payload["humidity"])

        return HttpResponse("Data received successfully.")
    else:
        return HttpResponse("Only POST requests are allowed.")