# Generated by Django 4.0.4 on 2022-08-20 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_category_cardpost_id_user_like_cardpost_id_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='EnglishLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='like',
            name='id_card',
            field=models.ForeignKey(blank=True, db_column='id_card', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_card', to='api.cardpost'),
        ),
    ]
