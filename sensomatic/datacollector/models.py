from django.db import models


class TrashIsland(models.Model):
    street_name = models.CharField(max_length=255)
    street_number = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.street_name} {self.street_number} - {self.zip_code}'


TRASH_TYPES = (
    (0, "Restaffald"),
    (1, "Glas"),
    (2, "Papir/Pap"),
    (3, "Metal/Plastik"),
    (4, "Batteri"),
    (5, "Elektronik"),

)


class Trashcan(models.Model):
    island = models.ForeignKey(TrashIsland, on_delete=models.SET_NULL, null=True)
    type = models.IntegerField(choices=TRASH_TYPES)
    capacity = models.IntegerField()
    fill_amount = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def get_type_display(self, ):
        return TRASH_TYPES[self.type][1]

    def __str__(self):
        return f'{self.island.street_name} {self.island.street_number} - {self.get_type_display()}'


class SensorData(models.Model):
    trashcan = models.ForeignKey(Trashcan, on_delete=models.SET_NULL, null=True)
    distance = models.FloatField(null=True, blank=True)
    fill_amount = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.trashcan} - {self.fill_amount}% full'

