import csv
import json
import geopy

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import SensorData, TrashIsland, Trashcan
from .greedy_2_opt import Run



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

@csrf_exempt
def sorting_algorithm(request):
    if request.method == "GET":
        Run()
        return JsonResponse({'message': 'Sorting algorithm executed'}, status = 200)
    


@csrf_exempt
def import_addresses(request):
    if request.method == "GET":
        """
        Fuld adresse,Materieltype,Antal,Tømningsdato
        Frederiksgade 6, 9000 Aalborg,Fuldt-nedgravet 5,0 m3 - offentlig (Restaffald),1.0,2/26/2024
        
        """
        with open('streets.csv', 'r') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                print(row)
                address = f'{row[0]} {row[1]}'
                location = geopy.geocoders.Nominatim(user_agent="Ch").geocode(address)
                if not location:
                    continue
                print(location)
                print(location.latitude)
                print(location.longitude)
                address = location.address.split(',')
                print(address)
                island, created = TrashIsland.objects.get_or_create(street_name=row[0], street_number=address[0], zip_code=row[1], latitude=location.latitude, longitude=location.longitude)
                Trashcan.objects.create(MAC_adress=i, time_interval=1, island=island, type=0, capacity=100, fill_percentage=0)
        return JsonResponse({'message': 'Addresses imported'}, status = 200)