# Generated by Django 4.2.16 on 2024-11-18 02:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0007_monthlysales_monthlysales_unique_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="regist_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="customuser",
            name="stripeCustomerId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="customuser",
            name="stripeSubscriptionId",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
