# Generated by Django 4.1 on 2022-10-17 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_cardpost_id_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardpost',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
