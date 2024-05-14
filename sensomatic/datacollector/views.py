import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import SensorData, TrashIsland, Trashcan
import sensomatic.datacollector.greedy_2_opt as greedy_2_opt


# Create your views here.

# til test af esp
@csrf_exempt
def handle_post(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        print("Received data:", payload)

        trashcan = Trashcan.objects.get(MAC_adress=payload["MAC"])

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

        SensorData.objects.create(trashcan=trashcan, distance=payload["distance"], fill_percentage=fill_percentage)
        trashcan.fill_percentage = fill_percentage
        trashcan.save()
        
        

        return JsonResponse({'sleepInterval': trashcan.time_interval}, status = 200)
    else:
        return JsonResponse({'message': 'Invalid request'}, status = 405)
    
def sorting_algorithm():
    full_trashcans = Trashcan.objects.filter(fill_percentage__gte=80).values()
    
