# Generated by Django 4.2.4 on 2024-02-19 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0018_remove_product_digital"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="digital",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
