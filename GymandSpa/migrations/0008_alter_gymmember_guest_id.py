# Generated by Django 4.2.3 on 2023-11-07 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Guest", "0001_initial"),
        ("GymandSpa", "0007_alter_gymmember_member_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gymmember",
            name="guest_id",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="Guest.guest"
            ),
        ),
    ]
