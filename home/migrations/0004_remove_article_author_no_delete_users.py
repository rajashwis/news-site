# Generated by Django 4.2.2 on 2023-06-27 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0003_alter_users_email_article"),
    ]

    operations = [
        migrations.RemoveField(model_name="article", name="author_no",),
        migrations.DeleteModel(name="Users",),
    ]
