# Generated by Django 4.1 on 2023-07-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0022_item_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]