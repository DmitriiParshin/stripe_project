from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=1500, blank=False)
    price = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.name
