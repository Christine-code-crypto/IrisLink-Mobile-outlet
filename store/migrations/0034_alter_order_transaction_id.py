# Generated by Django 4.2.4 on 2024-03-09 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0033_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transaction_id",
            field=models.CharField(max_length=100),
        ),
    ]
