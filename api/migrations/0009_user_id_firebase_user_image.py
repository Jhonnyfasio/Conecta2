# Generated by Django 4.1 on 2022-08-31 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_firebase',
            field=models.CharField(default='aaa', max_length=1000),
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.CharField(default='aaaa', max_length=5000),
        ),
    ]