# Generated by Django 4.0.4 on 2022-08-15 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='cardpost',
            name='id_user',
            field=models.ForeignKey(blank=True, db_column='id_user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_user', to='api.user'),
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField()),
                ('id_card', models.ForeignKey(blank=True, db_column='id_card', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_user', to='api.cardpost')),
                ('id_user', models.ForeignKey(blank=True, db_column='id_user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='like_user', to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='cardpost',
            name='id_category',
            field=models.ForeignKey(blank=True, db_column='id_category', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_categoryr', to='api.category'),
        ),
    ]
