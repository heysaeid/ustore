# Generated by Django 3.2.3 on 2021-06-27 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='postcode',
            new_name='postal_code',
        ),
    ]
