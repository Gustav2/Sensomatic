from django.contrib import admin

from .models import Route, AreaMaintenance

# Register your models here.
admin.site.register(Route)
admin.site.register(AreaMaintenance)