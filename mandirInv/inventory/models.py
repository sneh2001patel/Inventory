from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

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
    details = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='item_pics', blank=True, null=True, max_length=500)
    quantity = models.IntegerField()
    code = models.CharField(max_length=5)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    slug = AutoSlugField(populate_from='uid')

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse('inventory-update', kwargs={'pk': self.pk})


class Report(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    actual = models.IntegerField(blank=True)
    expected = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})
