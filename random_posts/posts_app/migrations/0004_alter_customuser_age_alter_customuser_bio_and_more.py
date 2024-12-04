# Generated by Django 5.1.3 on 2024-11-28 09:12

import posts_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0003_alter_customuser_managers"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="age",
            field=models.PositiveBigIntegerField(
                blank=True, null=True, validators=[posts_app.validators.validate_age]
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="bio",
            field=models.TextField(
                blank=True, validators=[posts_app.validators.validate_no_bad_words]
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=254,
                unique=True,
                validators=[posts_app.validators.validate_email],
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="categories",
            field=models.CharField(
                max_length=100, validators=[posts_app.validators.validate_no_bad_words]
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="content",
            field=models.TextField(
                validators=[
                    posts_app.validators.validate_no_bad_words,
                    posts_app.validators.validate_post_length,
                ]
            ),
        ),
    ]
