# Generated by Django 3.2.3 on 2021-06-22 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_order_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='final_price',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]