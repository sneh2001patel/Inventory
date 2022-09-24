from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.


class Area(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    uid = models.IntegerField()
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    code = models.CharField(max_length=5)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.code


class Report(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    expected = models.IntegerField()
    actual = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)