# Generated by Django 3.2.3 on 2021-06-22 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order_final_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='final_price',
            field=models.IntegerField(),
        ),
    ]
