# Generated by Django 5.1.5 on 2025-02-07 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("station", "0004_bus_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bus",
            name="facilities",
            field=models.ManyToManyField(
                blank=True, related_name="buses", to="station.facility"
            ),
        ),
    ]
