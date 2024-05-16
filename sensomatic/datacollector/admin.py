from django.contrib import admin

from .models import TrashIsland, Trashcan, SensorData

# Register your models here.
admin.site.register(TrashIsland)
class TrashcanAdmin(admin.ModelAdmin):
    list_display = ('island', 'fill_percentage')
admin.site.register(Trashcan, TrashcanAdmin)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('trashcan', 'fill_percentage', 'created_at')
admin.site.register(SensorData, SensorDataAdmin)