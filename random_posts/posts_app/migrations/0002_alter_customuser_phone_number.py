# Generated by Django 5.1.3 on 2024-12-13 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone_number",
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]