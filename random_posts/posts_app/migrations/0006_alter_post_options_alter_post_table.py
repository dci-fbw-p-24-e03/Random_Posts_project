# Generated by Django 5.1.3 on 2024-11-28 10:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("posts_app", "0005_alter_customuser_options_alter_customuser_table"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Post",
                "verbose_name_plural": "Posts",
            },
        ),
        migrations.AlterModelTable(
            name="post",
            table="posts",
        ),
    ]
