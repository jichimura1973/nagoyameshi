# Generated by Django 4.2.16 on 2024-10-13 00:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_alter_customuser_created_day_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="deleted_day",
            field=models.DateTimeField(blank=True, null=True, verbose_name="削除日"),
        ),
    ]