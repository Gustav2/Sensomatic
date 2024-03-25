from django.contrib import admin

from .models import TrashIsland, Trashcan, SensorData

# Register your models here.
admin.site.register(TrashIsland)
admin.site.register(Trashcan)
admin.site.register(SensorData)