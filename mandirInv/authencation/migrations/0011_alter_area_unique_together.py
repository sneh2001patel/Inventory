# Generated by Django 4.1 on 2023-06-21 15:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authencation', '0010_alter_user_area_incharge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='area',
            unique_together={('name', 'location')},
        ),
    ]
