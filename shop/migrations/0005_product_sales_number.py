# Generated by Django 3.2.3 on 2021-05-24 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_productgallery_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sales_number',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
