# Generated by Django 4.1.6 on 2023-02-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="price",
            field=models.IntegerField(default=0),
        ),
    ]
