# Generated by Django 3.2.5 on 2021-08-28 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_review_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sales_number',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
