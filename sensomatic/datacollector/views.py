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

        payload["distance"]

        trashisland = TrashIsland.objects.get(street_name="Test Street")
        trashcan = Trashcan.objects.get(island=trashisland)

        """
        **Test without this implementation and see if it works. 
        If not:
            Implement logic to determine the fill percentage of the container using 
            the container designation (size of the cointainer) and the distance measures by the sensor
        """

        capacity = trashcan.capacity
        empty_space = float(payload["distance"])
        fill_amount = capacity - empty_space
        fill_percentage = round((fill_amount / capacity) * 100, 2)

        SensorData.objects.create(trashcan=Trashcan.objects.get(id=1), distance=payload["distance"], fill_percentage=fill_percentage)
        trashcan.fill_percentage = fill_percentage
        trashcan.save()

        return HttpResponse("Data received successfully.")
    else:
        return HttpResponse("Only POST requests are allowed.")