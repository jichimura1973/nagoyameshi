# Generated by Django 4.2 on 2024-09-22 05:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0002_restaurant_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="close_day_of_week",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="定休日"
            ),
        ),
        migrations.AddField(
            model_name="restaurant",
            name="seats_number",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(1000),
                ],
                verbose_name="席数",
            ),
        ),
    ]
