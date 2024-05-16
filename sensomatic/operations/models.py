from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField
from geopy.geocoders import Nominatim
from time import sleep

# Create your models here.

# Her oprettes rute tabellen
class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    route_name = models.CharField(max_length=255, blank=False, null=False, default="Rute 1")
    adresses = models.TextField(blank=False, null=False)
    operating_date = models.DateField()
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
# Denne funktion henter coordinaterne og ændre de første og sidste til adresser
    def coordinate_to_adress(self):
        geolocator = Nominatim(user_agent="Chrome/122.0.0.0")
        adress_list =[]
        first_coordinate=self.adresses.split(";")[1]
        last_coordinate=self.adresses.rsplit(";")[2]

        first_adress = geolocator.reverse(first_coordinate)
        raw_firstadress = first_adress.raw
        first_adress_split = raw_firstadress['display_name'].split(",") 
        if len(first_adress_split)==8:
            first_adress_string = first_adress_split[1]+" "+first_adress_split[0]+","+first_adress_split[3]+first_adress_split[6]
        elif len(first_adress_split)==7:
            first_adress_string = first_adress_split[0]+first_adress_split[2]+first_adress_split[5]
        sleep(1)
        last_adress = geolocator.reverse(last_coordinate)
        raw_lastadress = last_adress.raw
        last_adress_split = raw_lastadress['display_name'].split(",")
        if len(last_adress_split)==8:
            last_adress_string = last_adress_split[1]+" "+last_adress_split[0]+","+last_adress_split[3]+last_adress_split[6]
        elif len(last_adress_split)==7:
            last_adress_string = last_adress_split[0]+last_adress_split[2]+last_adress_split[5]
        sleep(1)
        adress_list.append("Første affaldsø: " + first_adress_string)
        adress_list.append("Sidste affaldsø: " + last_adress_string)
        return adress_list
    


CATEGORY_CHOICES = (
    (0, "Stoppet indkastshul"),
    (1, "Småt skrald - oprydning"),
    (2, "Stort skrald - afhentning"),
    (3, "Andet"),
)

# Her oprettes en tabel for areamaintenance
class AreaMaintenance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    island = models.ForeignKey('datacollector.TrashIsland', on_delete=models.SET_NULL, null=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
