from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=1000)


class Category(models.Model):
    name = models.CharField(max_length=1000)


class CardPost(models.Model):
    content = models.CharField(max_length=1000)
    id_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                db_column='id_user', related_name='card_user')
    id_category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE,
                                    db_column='id_category', related_name='card_categoryr')


class Like(models.Model):
    status = models.BooleanField()
    id_user = models.ForeignKey(User, blank=True, null=False, on_delete=models.CASCADE,
                                db_column='id_user', related_name='like_user')
    id_card = models.ForeignKey(CardPost, blank=True, null=False, on_delete=models.CASCADE,
                                db_column='id_card', related_name='like_card')
