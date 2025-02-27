# Generated by Django 4.2.5 on 2023-11-05 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_alter_hotel_website'),
        ('GymandSpa', '0003_alter_gympackages_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='spa',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spabooking',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spafeedback',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spamember',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spapackage',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spaservice',
            name='hotel_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Authentication.hotel'),
            preserve_default=False,
        ),
    ]
