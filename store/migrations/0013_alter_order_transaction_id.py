# Generated by Django 4.2.4 on 2024-02-05 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_order_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transaction_id",
            field=models.CharField(default=173174.4567, max_length=100),
        ),
    ]
