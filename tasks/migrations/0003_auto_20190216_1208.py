# Generated by Django 2.1.7 on 2019-02-16 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190216_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='date_of_ending',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]