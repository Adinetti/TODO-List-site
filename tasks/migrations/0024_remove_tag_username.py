# Generated by Django 2.1.7 on 2019-03-06 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0023_auto_20190306_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='username',
        ),
    ]