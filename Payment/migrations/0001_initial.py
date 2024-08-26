# Generated by Django 4.2.3 on 2023-10-30 06:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Guest", "0001_initial"),
        ("Employee", "0001_initial"),
        ("Authentication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=300)),
                ("payment_detail", models.CharField(max_length=300)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hotel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.hotel",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("total", models.FloatField(default=0.0, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("Paid", "Paid"), ("Not paid", "Not paid")],
                        default="Not paid",
                        max_length=300,
                    ),
                ),
                ("received_amount", models.FloatField(default=0.0, null=True)),
                ("service_fee", models.FloatField(default=0.0, null=True)),
                ("discount", models.FloatField(default=0.0, null=True)),
                ("discount_reason", models.CharField(max_length=30)),
                ("change_returned", models.FloatField(default=0.0, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "confirmed_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Employee.employeeinfo",
                    ),
                ),
                (
                    "guest",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Guest.guest",
                    ),
                ),
                (
                    "hotel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.hotel",
                    ),
                ),
                (
                    "payment_method",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Payment.paymentmethod",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BankInfo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bank_name", models.CharField(max_length=300)),
                ("bank_branch", models.CharField(max_length=300)),
                ("bank_account_no", models.CharField(max_length=300)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "hotel_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Authentication.hotel",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
