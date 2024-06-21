# Generated by Django 4.2.4 on 2024-02-05 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0013_alter_order_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="complete",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="transaction_id",
            field=models.CharField(max_length=100),
        ),
    ]
