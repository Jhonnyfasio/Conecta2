# Generated by Django 4.0.2 on 2022-10-22 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_image_up'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.SlugField(default='aaa', max_length=170),
        ),
    ]