# Generated by Django 4.2.5 on 2023-10-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="weekdistance",
            name="week",
            field=models.DateField(null=True),
        ),
    ]
