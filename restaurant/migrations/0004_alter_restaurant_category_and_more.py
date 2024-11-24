# Generated by Django 4.2.16 on 2024-11-23 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0003_reservation_reservation_time_alter_review_visited_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="restaurant.category",
            ),
        ),
        migrations.AlterField(
            model_name="restaurantcategory",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="restaurant.category",
            ),
        ),
        migrations.AlterField(
            model_name="restaurantcategory",
            name="restaurant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to="restaurant.restaurant"
            ),
        ),
    ]
