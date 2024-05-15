from django.contrib import admin

from .models import TrashIsland, Trashcan, SensorData

# Register your models here.
admin.site.register(TrashIsland)
admin.site.register(Trashcan)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('trashcan', 'distance', 'created_at')
admin.site.register(SensorData, SensorDataAdmin)