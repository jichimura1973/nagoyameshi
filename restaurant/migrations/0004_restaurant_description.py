# Generated by Django 4.2 on 2024-09-22 06:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0003_restaurant_close_day_of_week_restaurant_seats_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="description",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="説明"
            ),
        ),
    ]
