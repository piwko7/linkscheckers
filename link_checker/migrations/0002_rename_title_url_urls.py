# Generated by Django 3.2.5 on 2021-08-01 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('link_checker', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='title',
            new_name='urls',
        ),
    ]
