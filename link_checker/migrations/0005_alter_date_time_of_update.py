# Generated by Django 3.2.5 on 2021-08-13 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link_checker', '0004_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='time_of_update',
            field=models.DateTimeField(),
        ),
    ]