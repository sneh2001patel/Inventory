from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django_extensions.db.fields import AutoSlugField

from authencation.models import Area

User = get_user_model()


# Create your models here.
class Item(models.Model):
    uid = models.IntegerField()
    description = models.CharField(max_length=200)
    details = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='item_pics', blank=True, null=True, max_length=500)
    quantity = models.IntegerField()
    code = models.CharField(max_length=5)
    area = models.ForeignKey(Area, null=True, on_delete=models.SET_NULL)
    slug = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.code + "-" + str(self.area.name) + "-" + str(self.area.location))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('inventory-update', kwargs={'pk': self.pk})


class Report(models.Model):
    uid = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    actual = models.IntegerField(blank=True)
    expected = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

    def get_absolute_url(self):
        return reverse('report-detail', kwargs={'pk': self.pk})


class ReportTable(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    date = models.DateField()
    reports = models.ManyToManyField(Report(), blank=True)
    viewed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['area', 'date'], name='unique_area_date_combination'
            )
        ]
