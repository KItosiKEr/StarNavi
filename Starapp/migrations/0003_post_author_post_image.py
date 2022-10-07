# Generated by Django 4.1.1 on 2022-10-04 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Starapp', '0002_post_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(default=11, upload_to='IM/%Y/%m'),
            preserve_default=False,
        ),
    ]
