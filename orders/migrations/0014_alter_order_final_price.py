# Generated by Django 3.2.5 on 2021-11-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20210828_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='final_price',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]