# Generated by Django 4.2.4 on 2024-03-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0026_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="phone",
            field=models.CharField(max_length=200, null=True),
        ),
    ]