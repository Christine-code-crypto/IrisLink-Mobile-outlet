# Generated by Django 4.2.4 on 2024-03-04 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0031_alter_order_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="transaction_id",
            field=models.CharField(default=1707160292.114927, max_length=100),
        ),
    ]