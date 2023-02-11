from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(max_length=1500)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
