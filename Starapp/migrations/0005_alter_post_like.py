# Generated by Django 3.2.7 on 2022-10-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Starapp', '0004_post_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
