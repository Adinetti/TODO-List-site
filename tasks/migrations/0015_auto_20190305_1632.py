# Generated by Django 2.1.7 on 2019-03-05 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20190228_1707'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='tags',
            new_name='tag',
        ),
    ]