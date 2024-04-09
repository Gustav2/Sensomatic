from django.contrib.auth.models import User
from django.db import models
from django.db.models import JSONField


# Create your models here.

class Route(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    adresses = models.TextField(blank=False, null=False)
    operating_date = models.DateField()
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def as_list(self):
        return self.adresses.split(",")


CATEGORY_CHOICES = (
    (0, "Stoppet indkastshul"),
    (1, "Småt skrald - oprydning"),
    (2, "Stort skrald - afhentning"),
    (3, "Andet"),
)


class AreaMaintenance(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    island = models.ForeignKey('datacollector.TrashIsland', on_delete=models.SET_NULL, null=True)
    category = models.IntegerField(choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
