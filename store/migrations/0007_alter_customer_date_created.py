# Generated by Django 4.2.4 on 2024-02-04 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0006_alter_customer_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="date_created",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
