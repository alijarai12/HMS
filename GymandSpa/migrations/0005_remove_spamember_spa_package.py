# Generated by Django 4.2.5 on 2023-11-05 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GymandSpa', '0004_spa_hotel_id_spabooking_hotel_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spamember',
            name='spa_package',
        ),
    ]
