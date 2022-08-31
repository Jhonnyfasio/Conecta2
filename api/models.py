from django.db import models

# Create your models here.


class EnglishLevel(models.Model):
    tag = models.CharField(max_length=10)


class User(models.Model):
    name = models.CharField(max_length=1000)
    email = models.EmailField(default='pedromorales@gmail.com')
    english_level = models.ForeignKey(EnglishLevel, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name='user_english_level')
    id_firebase = models.CharField(max_length=1000)
    image = models.CharField(max_length=5000)


class Category(models.Model):
    name = models.CharField(max_length=1000)


class CardPost(models.Model):
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='card_user')
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE,
                                 related_name='card_category')


class Like(models.Model):
    status = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='like_user')
    card = models.ForeignKey(CardPost, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='like_card')


class Save(models.Model):
    status = models.BooleanField()
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='save_user')
    card = models.ForeignKey(CardPost, blank=True, null=True, on_delete=models.CASCADE,
                             related_name='save_card')
