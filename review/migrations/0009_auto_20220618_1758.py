# Generated by Django 3.2.13 on 2022-06-18 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0008_review_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='name',
        ),
        migrations.AddField(
            model_name='review',
            name='slug',
            field=models.SlugField(allow_unicode=True, default=1, max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
