# Generated by Django 3.2.13 on 2022-06-18 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0009_auto_20220618_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='slug',
            field=models.CharField(db_index=True, max_length=20),
        ),
    ]
