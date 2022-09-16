from django.db import models


# Create your models here.
class Area(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.category
