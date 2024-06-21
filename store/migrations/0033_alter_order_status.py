# Generated by Django 4.2.4 on 2024-03-05 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0032_alter_order_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Delivered", "Delivered")],
                max_length=200,
                null=True,
            ),
        ),
    ]
