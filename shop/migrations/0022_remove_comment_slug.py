# Generated by Django 3.2.13 on 2022-06-20 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_auto_20220620_1738'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='slug',
        ),
    ]
