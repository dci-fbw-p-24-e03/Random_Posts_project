# Generated by Django 5.1.3 on 2024-11-28 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0004_alter_customuser_age_alter_customuser_bio_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="customuser",
            options={
                "ordering": ["username"],
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.AlterModelTable(
            name="customuser",
            table="random_posts_users",
        ),
    ]
