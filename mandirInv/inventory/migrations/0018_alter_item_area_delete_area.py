# Generated by Django 4.1 on 2023-04-01 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authencation', '0005_area_remove_user_area_incharge_user_area_incharge'),
        ('inventory', '0017_remove_report_id_alter_report_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authencation.area'),
        ),
        migrations.DeleteModel(
            name='Area',
        ),
    ]
