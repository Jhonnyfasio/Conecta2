# Generated by Django 4.0.4 on 2022-08-20 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_englishlevel_alter_like_id_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='id_english_level',
            field=models.ForeignKey(blank=True, db_column='id_english_level', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_english_level', to='api.englishlevel'),
        ),
        migrations.AlterField(
            model_name='cardpost',
            name='id_category',
            field=models.ForeignKey(blank=True, db_column='id_category', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='card_category', to='api.category'),
        ),
    ]