import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import SensorData, TrashIsland, Trashcan


# Create your views here.

@csrf_exempt
def gateway(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        trashisland = TrashIsland.objects.get(street_name="Test Street")
        trashcan = Trashcan.objects.get(island=trashisland)

        SensorData.objects.create(trashcan=trashcan, status=data['status'])

        return HttpResponse("")
